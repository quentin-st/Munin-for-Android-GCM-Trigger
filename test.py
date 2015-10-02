#!/usr/bin/python
# -*- coding: utf-8 -*-
import sys
import requests
import json
from devices import devices
from main import GCM_PROXY_TEST_URL


# Check if there are devices
if len(devices) == 0:
    raise Exception('Empty devices list. Define devices in devices.py')

# There are devices! Send the test request to proxy

# Send information to GCM proxy
request = requests.post(GCM_PROXY_TEST_URL, data={
    'reg_ids': json.dumps(devices)
})
