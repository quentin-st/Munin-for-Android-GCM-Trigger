#!/usr/bin/python
# -*- coding: utf-8 -*-
import sys
import requests
import json
from devices import devices
from const import GCM_PROXY_TEST_URL

if __name__ == '__main__':

    # Check if there are devices
    if len(devices) == 0:
        raise Exception('Empty devices list. Define devices in devices.py')

    # There are devices! Send the test request to proxy

    # Send information to GCM proxy
    response = requests.post(GCM_PROXY_TEST_URL, data={
        'reg_ids': json.dumps(devices)
    })

    try:
        response.raise_for_status()
    except requests.exceptions.HTTPError as e:
        print "HTTP error: ", e.message
