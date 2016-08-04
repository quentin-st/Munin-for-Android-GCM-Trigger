#!/usr/bin/python3
# -*- coding: utf-8 -*-

GCM_PROXY_URL = 'https://gcm-proxy.munin-for-android.com/trigger/declareAlert'
GCM_PROXY_TEST_URL = 'https://gcm-proxy.munin-for-android.com/trigger/test'

# If true, the server will temporary store the XML structure for debugging purposes if it failed parsing it _only_
HELP_DIAGNOSE = False
# If true, we'll increment our "notifications sent" counter when a notification is sent.
# We won't store any information about the notification.
CONTRIBUTE_TO_STATS = True
