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

from nltk.tokenize.moses import MosesDetokenizer
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


def wait(seconds):
    '''
    waits and prints a friendly message to stderr

    Parameters:
    -----------
        seconds : int
            number of seconds to wait
    '''
    print("waiting {} seconds".format(seconds),
          end='', file=stderr, flush=True)
    for i in range(seconds):
        time.sleep(1)
        print(".", end='', file=stderr, flush=True)
    print("", file=stderr, flush=True)


class Recognizer():
    '''
    Recognizer class

    Parameters:
    -----------
        config_file : str
            path to config file containing url and subscription key for API
        handwriting_param : str
            parameter that takes str values of 'true' or 'false' to be passed
            to API indicating whether to do handwriting recognition ('true')
            or OCR ('false')
        keep_tokenization : boolean (Default True)
            Azure provides tokenized output.  By default this output is
            detokenized using the Moses detokenizer. When keep_tokenization is
            True, the tokenization of the output will be preserved
    '''
    def __init__(self, config_file, handwriting_param, keep_tokenization):

        assert (handwriting_param == 'true' or handwriting_param == 'false')

        self.config_file = config_file
        self.handwriting_param = handwriting_param
        self.keep_tokenization = keep_tokenization

        # if we are not keeping the tokenization, we'll need an instance of the
        # detokenizer, and let's alias the detokenize function as well
        if not keep_tokenization:
            self.detokenizer = MosesDetokenizer()
            self.detokenize = self.detokenizer.detokenize

        self._request_params = {'handwriting': handwriting_param}
        self.parse_config_file()

    def __repr__(self):
        return "Recognizer(config_file='{}', handwriting_param='{}')".format(
                    self.config_file, self.handwriting_param)

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

    def get_hwr_text_result(self, operation_location):
        """
        Helper function to get text result from operation location after API
        call for Handwriting Recognition.  (This is not necessary in the case
        of OCR.)

        Parameters:
        ------------
            operation_location: operationLocation to get text result

        Returns:
        --------
            result : json
        """
        print('retrieving HWR results from server', file=stderr, flush=True)
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
                    "rate limit has been exceeded." So we find out how long it
                    wants us to wait, and we wait.
                    '''
                    message = response.json()['message']
                    waittime = re.search(r'Try again in (\d+) seconds',
                                         message).group(1)
                    wait(int(waittime))
                except (AttributeError, KeyError):
                    pass

                if retries <= self._max_num_retries:
                    time.sleep(1)
                    retries += 1
                    continue
                else:
                    print('Error: failed retrieval after retrying '
                          '{} times!'.format(self._max_num_retries),
                          file=stderr, flush=True)
                    break
            elif response.status_code == 200:
                result = response.json()
                status = result['status']
                if status == 'Succeeded' or status == 'Failed':
                    break
                else:
                    # it could have a status of 'Running', so we wait a sec
                    time.sleep(1)
            else:
                print("Error code: %d" % (response.status_code),
                      file=stderr, flush=True)
                print("Message: %s" % (response.json()),
                      file=stderr, flush=True)
                break

        return result

    def extract_hwr_text_from_json(self, result):
        '''
        return a list of lines from the result json with we're doing
        handwriting.
        '''
        lines = [line['text']
                 for line
                 in result['recognitionResult']['lines']]

        if self.keep_tokenization:
            return lines
        else:
            return [" ".join(self.detokenize(line.split()))
                    for line in lines]

    def extract_ocr_text_from_json(self, result):
        '''
        return a list of lines from the result json when we're doing ocr
        '''
        output_lines = []

        for region in result['regions']:
            for line in region['lines']:
                words = [word['text'] for word in line['words']]

                if self.keep_tokenization:
                    output_lines.append(" ".join(words))
                else:
                    output_lines.append(" ".join(self.detokenize(words)))

        return output_lines

    def process_response(self, response):
        '''
        process the response from the API call as appropriate for either OCR
        or handwriting recognition.

        In the case of OCR, response.json contains the recognition result
        directly.  In the case of handwriting recognition, the response has an
        'OperationLocation' header which will indicate a URL for our
        recognition result, and this will have to be retreived in a separate
        request

        Parameter:
        ---------
            response : requests.models.Response
                response from API call

        Returns:
            result : dict
                json result of API call
        '''

        if self.handwriting_param == 'false':
            result = response.json()
        else:
            operation_location = response.headers['Operation-Location']
            result = self.get_hwr_text_result(operation_location)

        return result

    def submit_request(self, data):
        """
        Helper function to process the request to API

        Parameters:
        -----------
            data : bytes
                bytes representing image read from disk.

        Returns:
        --------
            response : requests.models.Response
                response.json() will will have an 'Operation-Location' header
                in the case of handwriting recognition, which will have to be
                retrived; in the case of OCR, it will have the recognition
                result directly.
        """
        print('submitting request to API.', file=stderr, flush=True)

        retries = 0
        result = None

        while True:
            response = requests.request('post', self._url, data=data,
                                        headers=self._headers,
                                        params=self._request_params)

            if response.status_code == 429:
                print(response.json(), file=stderr, flush=True)
                try:
                    '''
                    It looks like sometimes this is a message saying that the
                    "rate limit has been exceeded." So we find out how long it
                    wants us to wait, and we wait.
                    '''
                    message = response.json()['message']
                    waittime = re.search(r'Try again in (\d+) seconds',
                                         message).group(1)
                    wait(int(waittime))
                except (AttributeError, KeyError):
                    pass

                if retries <= self._max_num_retries:
                    time.sleep(1)
                    retries += 1
                    continue
                else:
                    print('Error: failed request after retrying '
                          '{} times!'.format(self._max_num_retries),
                          file=stderr, flush=True)
                    break

            elif response.status_code == 200 or response.status_code == 202:
                # it looks like success is indicated by status_code 200 in the
                # case of OCR, but 202 in the case of handwriting recognition
                result = self.process_response(response)
                break
            else:
                print("Error code: %d" % (response.status_code),
                      file=stderr, flush=True)
                print("Message: %s" % (response.json()),
                      file=stderr, flush=True)
                break

        return result

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
        result = self.submit_request(data)

        if result:

            # get a list of output lines (This is the output OCR text!)
            # the structure of the result json is very different depending on
            # if we're doing ocr or hwr.  We have two separate parsing
            # functions:

            if self.handwriting_param == 'true':
                output_lines = self.extract_hwr_text_from_json(result)
                output_image = get_output_image(result, data)
                return (output_image, output_lines, result)
            else:
                output_lines = self.extract_ocr_text_from_json(result)
                # we do not construct an output image for OCR.
                # It's too messy anyway, and the json is different
                return (None, output_lines, result)
        else:

            return (None, None, None)


def process_image_file(image_file, recognizer, output_directory,
                       output_json=False):
    '''
    read in a file and process it, calling the API

    Parameters:
    -----------
        image_file : str
            path to image file
        recognizer : Recognizer
        output_directory : str
        output_json : boolean (default False)
            output json file with recognition results and bounding box
            locations when True
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

        # and save the output:
        if output_image_plt:
            # (it's only here if we're doing hwr and not ocr)
            output_image_plt.savefig(output_image_file, bbox_inches='tight')
            print("output", output_image_file, file=stderr, flush=True)

        # output the json if we were asked to
        if output_json:
            with open(output_json_file, "w") as f:
                json.dump(result_json, f)
            print("output", output_json_file, file=stderr, flush=True)

        # and finally the text output
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
        description="Submit images to Microsoft Azure Text Recognition API")
    parser.add_argument('config_file',
                        help="config file containing API URL and "
                             "path to file containing subscription key")
    input_group = parser.add_mutually_exclusive_group(required=True)
    input_group.add_argument('-i', '--input_image',
                             help='path to input_image')
    input_group.add_argument('-f', '--file_of_input_paths',
                             help='file containing paths to input images, '
                             'with each path on a new line')
    parser.add_argument('-o', '--output_directory', help="defaults to curdir",
                        default=path.curdir, nargs="?")
    parser.add_argument('-r', '--ocr', action='store_true', default=False,
                        help='Do OCR on typewritten text instead of '
                             'recognizing handwritten text. (Default is to '
                             'recognize handwritten text')
    parser.add_argument('-k', '--keep_tokenization', action='store_true',
                        default=False,
                        help='Azure provides tokenized output.  By default, '
                             'this output is detokenized using the Moses '
                             'detokenizer. Passing this flag will preserve '
                             'the tokenization of the output.')
    parser.add_argument('-j', '--json', action='store_true',
                        default=False,
                        help='Output json file with recognition results and '
                             'bounding boxes.  May be useful for debugging.')
    args = parser.parse_args()

    # set up recognizer for either OCR or handwritting recognition with
    # parameters from config file
    handwriting_param = 'false' if args.ocr else 'true'
    recognizer = Recognizer(args.config_file,
                            handwriting_param,
                            args.keep_tokenization)

    if args.input_image:
        # process a single image
        process_image_file(args.input_image,
                           recognizer,
                           args.output_directory,
                           args.json)
    else:
        # we have a file of paths to work with; process a batch
        with open(args.file_of_input_paths) as f:
            for line in f.readlines():
                line = line.strip()
                if line:
                    try:
                        process_image_file(line,
                                           recognizer,
                                           args.output_directory,
                                           args.json)
                    except FileNotFoundError as e:
                        print(e, file=stderr)


if __name__ == '__main__':
    main()
