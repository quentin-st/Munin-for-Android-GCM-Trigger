#!/usr/bin/python
# -*- coding: utf-8 -*-
import sys
import requests
import json
import argparse
from devices import devices
from const import GCM_PROXY_URL, GCM_PROXY_TEST_URL

if __name__ == '__main__':

    # Check if there are devices
    if len(devices) == 0:
        raise Exception('Empty devices list. Define devices in devices.py')

    parser = argparse.ArgumentParser(description='Receive alerts from munin and relay them to Google Cloud Messaging')
    parser.add_argument("--test", action="store_true", dest="test", default=False)
    args = parser.parse_args()

    if args.test:
        # Send a test message to GCM. A success notification will be displayed on each device
        response = requests.post(GCM_PROXY_TEST_URL, data={
            'reg_ids': json.dumps(devices)
        })

        try:
            response.raise_for_status()
        except requests.exceptions.HTTPError as e:
            print "HTTP error: ", e.message
    else:
        std_input = ''
        for line in sys.stdin:
            std_input += line

        response = requests.post(GCM_PROXY_URL, data={
            'reg_ids': json.dumps(devices),
            'data': std_input
        })
