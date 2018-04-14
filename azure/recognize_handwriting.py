#!/usr/bin/env python3

import argparse
import cv2
import json
import numpy as np
import operator
import re
import requests
import time
import yaml

import matplotlib.pyplot as plt
from matplotlib.lines import Line2D
from os import mkdir, path
from sys import stderr


def get_output_image(result_json, data):
    '''
    return a pyplt image in which the OCR hypothesis in result_json has been
    superimposed in their corresponding locations over the image represented
    by data

    Parameters:
    -----------
        result_json : dict
            json result as returned from api

        data : bytes
            bytes representing the image

    Returns:
    --------
        plt : pyplot
            matplotlib image in which OCR hypothesis have been superimposed
    '''
    print("preparing output image.", file=stderr, flush=True)

    # convert string to an unsigned int array
    data8uint = np.fromstring(data, np.uint8)
    # copy-and-paste from notebook.  Not sure what all these paramters do
    img = cv2.cvtColor(cv2.imdecode(data8uint, cv2.IMREAD_COLOR),
                       cv2.COLOR_BGR2RGB)

    # this is all copy-and-paste from notebook.
    img = img[:, :, (2, 1, 0)]
    fig, ax = plt.subplots(figsize=(12, 12))
    ax.imshow(img, aspect='equal')

    lines = result_json['recognitionResult']['lines']

    for i in range(len(lines)):
        words = lines[i]['words']
        for j in range(len(words)):
            tl = (words[j]['boundingBox'][0], words[j]['boundingBox'][1])
            tr = (words[j]['boundingBox'][2], words[j]['boundingBox'][3])
            br = (words[j]['boundingBox'][4], words[j]['boundingBox'][5])
            bl = (words[j]['boundingBox'][6], words[j]['boundingBox'][7])
            text = words[j]['text']
            x = [tl[0], tr[0], tr[0], br[0], br[0], bl[0], bl[0], tl[0]]
            y = [tl[1], tr[1], tr[1], br[1], br[1], bl[1], bl[1], tl[1]]
            line = Line2D(x, y, linewidth=3.5, color='red')
            ax.add_line(line)
            ax.text(tl[0], tl[1] - 2, '{:s}'.format(text),
                    bbox=dict(facecolor='blue', alpha=0.5),
                    fontsize=14, color='white')

    plt.axis('off')
    plt.tight_layout()
    plt.draw()

    return plt


class HandwritingRecognizer():
    '''
    HandwritingRecognizer class

    Parameters:
    -----------
        config_file : str
            path to config file containing url and subscription key for API
    '''
    def __init__(self, config_file):
        self.config_file = config_file
        self._request_params = {'handwriting': 'true'}
        self.parse_config_file()

    def __repr__(self):
        return "HandwritingRecognizer(config_file={}".format(self.config_file)

    def parse_config_file(self):
        '''
        Parse config file and set attributes
        '''
        with open(self.config_file, 'r') as f:
            config = yaml.load(f)

        # url to make Azure API call
        self._url = config['url']

        # path to subscription key for Azure API
        key_path = config['key_file']
        with open(key_path) as f:
            self._key = f.read().strip()

        self._max_num_retries = config['max_num_retries']

        self._headers = {'Ocp-Apim-Subscription-Key': self._key,
                         'Content-Type': 'application/octet-stream'}

        # does it matter if 'Content-Type' is there?
        self._retrieval_headers = {'Ocp-Apim-Subscription-Key': self._key}

    def submit_request(self, data):
        """
        Helper function to process the request to API
        copy-and-paste-and modify from the notebook

        Parameters:
        -----------
            data : bytes
                bytes representing image read from disk.

        Returns:
        --------
            operation_location : str
                operation location (url) from which OCR result can be retrieved
        """
        print('submitting request to API.', file=stderr, flush=True)

        retries = 0
        operation_location = None

        while True:
            response = requests.request('post', self._url, data=data,
                                        headers=self._headers,
                                        params=self._request_params)

            if response.status_code == 429:
                print(response.json(), file=stderr, flush=True)
                try:
                    '''
                    It looks like sometimes this is a message saying that the
                    "rate limit has been exceeded."" So we find out how long it
                    wants us to wait, and we wait.
                    '''
                    message = response.json()['message']
                    waittime = re.search(r'Try again in (\d+) seconds',
                                         message).group(1)
                    print("waiting {} seconds".format(waittime), file=stderr)
                    time.sleep(int(waittime))
                except (AttributeError, KeyError):
                    pass

                if retries <= self._max_num_retries:
                    time.sleep(1)
                    retries += 1
                    continue
                else:
                    print('Error: failed after retrying {} times!'.format(
                                                        self._max_num_retries),
                          file=stderr, flush=True)
                    break
            elif response.status_code == 202:
                operation_location = response.headers['Operation-Location']
            else:
                print("Error code: %d" % (response.status_code),
                      file=stderr, flush=True)
                print("Message: %s" % (response.json()),
                      file=stderr, flush=True)
            break
        return operation_location

    def get_text_result(self, operation_location):
        """
        Helper function to get text result from operation location after API
        call.  Mostly a copy-and-paste from notebook

        Parameters:
        ------------
            operation_location: operationLocation to get text result
        """
        retries = 0
        result = None

        while True:
            response = requests.request('get', operation_location,
                                        headers=self._retrieval_headers)
            if response.status_code == 429:
                print(response.json(), file=stderr, flush=True)
                try:
                    '''
                    It looks like sometimes this is a message saying that the
                    "rate limit has been exceeded."" So we find out how long it
                    wants us to wait, and we wait.
                    '''
                    message = response.json()['message']
                    waittime = re.search(r'Try again in (\d+) seconds',
                                         message).group(1)
                    print("waiting {} seconds".format(waittime), file=stderr)
                    time.sleep(int(waittime))
                except (AttributeError, KeyError):
                    pass

                if retries <= self._max_num_retries:
                    time.sleep(1)
                    retries += 1
                    continue
                else:
                    print('Error: failed after retrying {} times!'.format(
                                                        self._max_num_retries),
                          file=stderr, flush=True)
                    break
            elif response.status_code == 200:
                result = response.json()
            else:
                print("Error code: %d" % (response.status_code),
                      file=stderr, flush=True)
                print("Message: %s" % (response.json()),
                      file=stderr, flush=True)
            break

        return result

    def extract_text_from_json(self, result):
        '''
        return a list of lines from the result json
        '''
        return [line['text']
                for line
                in result['recognitionResult']['lines']]

    def process_image_data(self, data):
        '''
        make the API call and return the result

        Parameters:
        -----------
            data : bytes
                bytes comprising the image

        Returns:
        --------
            output_image : pyplt
                matplotlib figure of original image with OCR hypotheses
                superimposed in their locations
            output_lines : list of str
                list of OCR hypotheses corresponding to lines
            result : dict
                json representing the API response.
        '''
        result = None
        operation_location = self.submit_request(data)

        if operation_location is not None:

            print('retrieving results from server', file=stderr, flush=True)

            while True:
                result = self.get_text_result(operation_location)

                if (result['status'] == 'Succeeded'
                        or result['status'] == 'Failed'):
                    break

                time.sleep(1)

            # get a list of output lines (This is the output OCR text!)
            output_lines = self.extract_text_from_json(result)

            output_image = get_output_image(result, data)

            return (output_image, output_lines, result)
        else:
            return (None, None, None)


def process_image_file(image_file, recognizer, output_directory):
    '''
    read in a file and process it, calling the API

    Parameters:
    -----------
        image_file : str
            path to image file
        recognizer : HandwritingRecognizer
        output_directory : str
    '''

    # read in the image data as bytes
    print("processing", image_file, file=stderr)

    with open(image_file, 'rb') as f:
        data = f.read()

    # process the image and make API call
    output_image_plt, text, result_json = recognizer.process_image_data(data)

    if text is not None:
        # prepare output filenames
        basename = path.splitext(path.basename(image_file))[0]

        output_image_file = path.join(output_directory,
                                      basename + ".annotated.png")
        output_json_file = path.join(output_directory, basename + ".json")
        output_text_file = path.join(output_directory,
                                     basename + ".recognized.txt")

        # let's make sure out output directory is there
        if not path.isdir(output_directory):
            mkdir(output_directory)

        # and save the output
        output_image_plt.savefig(output_image_file, bbox_inches='tight')
        print("output", output_image_file, file=stderr, flush=True)

        with open(output_json_file, "w") as f:
            json.dump(result_json, f)
        print("output", output_json_file, file=stderr, flush=True)

        with open(output_text_file, "w") as f:
            for line in text:
                print(line, file=f)
        print("output", output_text_file, file=stderr, flush=True)
    else:
        # there was some issue with the API call.  An error would have printed
        # to stderr by now.
        print("No output retreived for ", image_file, file=stderr, flush=True)


def main():
    # set up argument parser
    parser = argparse.ArgumentParser(
        description="quick and dirty wrapper for Microsoft Azure Handwriting "
                    "Recognition API")
    parser.add_argument('config_file',
                        help="config file containing API URL and "
                             "path to file containing subscription key")
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument('-i', '--input_image',
                       help='path to input_image')
    group.add_argument('-f', '--file_of_input_paths',
                       help='file containing paths to input images, with '
                             'each path on a new line')
    parser.add_argument('output_directory', help="defaults to curdir",
                        default=path.curdir, nargs="?")
    args = parser.parse_args()

    # set up recognizer with parameters from config file
    recognizer = HandwritingRecognizer(args.config_file)

    if args.input_image:
        # process a single image
        process_image_file(args.input_image,
                           recognizer,
                           args.output_directory)
    else:
        # we have a file of paths to work with; process a batch
        with open(args.file_of_input_paths) as f:
            for line in f.readlines():
                line = line.strip()
                if line:
                    try:
                        process_image_file(line,
                                           recognizer,
                                           args.output_directory)
                    except FileNotFoundError as e:
                        print(e, file=stderr)


if __name__ == '__main__':
    main()
