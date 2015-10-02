#!/usr/bin/python
# -*- coding: utf-8 -*-
import sys
import requests
import json
from devices import devices

GCM_PROXY_URL = 'http://gcm-proxy.munin-for-android.com/trigger/declareAlert'
GCM_PROXY_TEST_URL = 'http://gcm-proxy.munin-for-android.com/trigger/test'


# Check if there are devices
if len(devices) == 0:
    raise Exception('Empty devices list. Define devices in devices.py')

# There are devices! Read std input for munin report:
std_input = ''
for line in sys.stdin:
    std_input += line

# Send information to GCM proxy
request = requests.post(GCM_PROXY_URL, data={
    'reg_ids': json.dumps(devices),
    'data': std_input
})
