#!/usr/bin/python3
# -*- coding: utf-8 -*-
import sys
import os
import requests
import json
import argparse
import shutil
from const import GCM_PROXY_URL, GCM_PROXY_TEST_URL, HELP_DIAGNOSE, CONTRIBUTE_TO_STATS

devices_filename = 'devices.json'
devices_filename_old = 'devices.py'
devices_filename_old_bak = 'devices.py.bak'


def migrate():
    # Migrate from devices.py to devices.json
    if not os.path.isfile(devices_filename_old):
        print('Could not find {}, aborting'.format(devices_filename_old))
        sys.exit(1)

    from devices import devices
    with open(devices_filename, 'w') as json_fh:
        json.dump({'devices': devices}, json_fh, indent=4)

    # Backup old file
    shutil.move(devices_filename_old, devices_filename_old_bak)

    print('Migrated from {} to {} with {} device(s)'.format(devices_filename_old, devices_filename, len(devices)))
    print('{} has been moved to {}'.format(devices_filename_old, devices_filename_old_bak))


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Receive alerts from munin and relay them to Google Cloud Messaging')
    parser.add_argument("--test", action="store_true", dest="test", default=False)
    parser.add_argument("--migrate", action="store_true", dest="migrate", default=False)
    args = parser.parse_args()

    if args.migrate:
        migrate()
    else:
        if os.path.isfile(devices_filename_old):
            # Silently migrate from old format to new one
            migrate()

        # Parse devices list
        with open(devices_filename, 'r') as file:
            try:
                devices = json.load(file)['devices']
            except ValueError as e:
                print('Could not parse {}, please check its syntax'.format(devices_filename))
                print(e)
                sys.exit(1)

        if len(devices) == 0:
            print('{} is empty, aborting'.format(devices_filename))
            sys.exit(1)

        if args.test:
            # Send a test message to GCM. A success notification will be displayed on each device
            response = requests.post(GCM_PROXY_TEST_URL, data={
                'reg_ids': json.dumps(devices)
            })

            try:
                status = response.raise_for_status()

                print('Successfully sent a test notification to your {} device(s)'.format(len(devices)))
            except requests.exceptions.HTTPError as e:
                print("HTTP error: ", e.response)
        else:
            data = ''.join(sys.stdin.readlines())

            # Wrap XML structure inside a single node:
            # <alert /><alert /> becomes <a><alert /><alert /></a>
            std_input = '<a>' + data + '</a>'

            response = requests.post(GCM_PROXY_URL, data={
                'reg_ids': json.dumps(devices),
                'data': std_input,
                'help_diagnose': HELP_DIAGNOSE,
                'contribute_to_stats': CONTRIBUTE_TO_STATS
            })
