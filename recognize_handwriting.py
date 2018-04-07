#!/usr/bin/env python3

import argparse
import cv2
import numpy as np
import operator
import requests
import time
import yaml

import matplotlib.pyplot as plt
from matplotlib.lines import Line2D


class HandwritingRecognizer():
    def __init__(self, config_file):
        self.config_file = config_file
        self._request_params = {'handwriting': 'true'}
        self.parse_config_file()

    def __repr__(self):
        return "HandwritingRecognizer(config_file={}".format(self.config_file)

    def parse_config_file(self):
        with open(self.config_file, 'r') as f:
            config = yaml.load(f)

        self._url = config['url']

        key_path = config['key_file']
        with open(key_path) as f:
            self._key = f.read().strip()

        self._max_num_retries = config['max_num_retries']

        self._headers = {'Ocp-Apim-Subscription-Key': self._key,
                         'Content-Type': 'application/octet-stream'}

        # does it matter if 'Content-Type' is there?
        self._retrieval_headers = {'Ocp-Apim-Subscription-Key': self._key}

    def process_request(self, data):
        """
        Helper function to process the request to API
        copy-and-paste-and modify from the notebook

        Parameters:
        data: Used when processing image read from disk. See API Documentation
        """

        retries = 0
        result = None

        while True:
            response = requests.request('post', self._url, data=data,
                                        headers=self._headers,
                                        params=self._request_params)

            if response.status_code == 429:
                print("Message: %s" % (response.json()))
                if retries <= self._max_num_retries:
                    time.sleep(1)
                    retries += 1
                    continue
                else:
                    print('Error: failed after retrying {} times!'.format(
                                                        self._max_num_retries))
                    break
            elif response.status_code == 202:
                result = response.headers['Operation-Location']
            else:
                print("Error code: %d" % (response.status_code))
                print("Message: %s" % (response.json()))
            break
        return result

    def get_text_result(self, operation_location):
        """
        Helper function to get text result from operation location

        Parameters:
        operationLocation: operationLocation to get text result, See API Documentation
        """
        retries = 0
        result = None

        while True:
            response = requests.request('get', operation_location,
                                        headers=self._retrieval_headers)
            if response.status_code == 429:
                print("Message: %s" % (response.json()))
                if retries <= self._max_num_retries:
                    time.sleep(1)
                    retries += 1
                    continue
                else:
                    print('Error: failed after retrying {} times!'.format(
                                                        self._max_num_retries))
                    break
            elif response.status_code == 200:
                result = response.json()
            else:
                print("Error code: %d" % (response.status_code))
                print("Message: %s" % (response.json()))
            break

        return result

    def extract_text_from_json(result):
        '''
        return a list of lines from the result json

        '''
        return [line['text']
                for line
                in result['recognitionResult']['lines']]

    def process_image(self, data):
        '''
        make the API call and return the result

        Parameters:
        -----------
            data : bytes
                bytes comprising the image

        Returns:
        --------
        '''
        result = None
        operation_location = self.process_request(data)

        if operation_location is not None:
            while True:
                result = self.get_text_result(operation_location)

                if (result['status'] == 'Succeeded'
                        or result['status'] == 'Failed'):
                    break

                time.sleep(1)

        # get a list of output lines (This is the output OCR text!)
        output_lines = self.get_text_result


def main():
    parser = argparse.ArgumentParser(
        description="quick and dirty wrapper for Microsoft Azure Handwriting "
                    "Recognition API")
    parser.add_argument('config_file',
                        help="config file containing API URL and "
                             "subscription key")
    parser.add_argument('input_image')
    args = parser.parse_args()

    recognizer = HandwritingRecognizer(args.config_file)

    with open(args.input_image, 'rb') as f:
        data = f.read()

    output_image, text = recognizer.process_image(data)



if __name__ == '__main__':
    main()
