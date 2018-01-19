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
devices_filename_default = 'devices_default.json'
devices_filename_old = 'devices.py'
devices_filename_old_bak = 'devices.py.bak'

self_path = os.path.dirname(__file__)
devices_filepath = os.path.join(self_path, devices_filename)
devices_filepath_default = os.path.join(self_path, devices_filename_default)
devices_filepath_old = os.path.join(self_path, devices_filename_old)
devices_filepath_old_bak = os.path.join(self_path, devices_filename_old_bak)


def get_devices():
    if not os.path.isfile(devices_filepath):
        # Silently initialize the devices file from the default one
        shutil.copyfile(devices_filepath_default, devices_filepath)

    if os.path.isfile(devices_filepath_old):
        # Silently migrate from old format to new one
        migrate()

    # Parse devices list
    with open(devices_filepath, 'r') as file:
        try:
            return json.load(file)['devices']
        except ValueError as e:
            print('Could not parse {}, please check its syntax'.format(devices_filename))
            print(e)
            return None


def do_test(test_devices):
    # Send a test message to GCM. A success notification will be displayed on each device
    response = requests.post(GCM_PROXY_TEST_URL, data={
        'reg_ids': json.dumps(test_devices)
    })

    try:
        status = response.raise_for_status()

        print('Successfully sent a test notification to {} device(s)'.format(len(test_devices)))
    except requests.exceptions.HTTPError as e:
        print("HTTP error: ", e.response)


def ask_yes_no(question, default="yes"):
    """Ask a yes/no question via raw_input() and return their answer.

    "question" is a string that is presented to the user.
    "default" is the presumed answer if the user just hits <Enter>.
        It must be "yes" (the default), "no" or None (meaning
        an answer is required of the user).

    The "answer" return value is True for "yes" or False for "no".
    http://code.activestate.com/recipes/577058/
    """
    valid = {"yes": True, "y": True, "ye": True,
             "no": False, "n": False}
    if default is None:
        prompt = " [y/n] "
    elif default == "yes":
        prompt = " [Y/n] "
    elif default == "no":
        prompt = " [y/N] "
    else:
        raise ValueError("invalid default answer: '%s'" % default)

    while True:
        sys.stdout.write(question + prompt)

        if sys.version_info.major == 2:
            choice = raw_input().lower()
        else:
            choice = input().lower()

        if default is not None and choice == '':
            return valid[default]
        elif choice in valid:
            return valid[choice]
        else:
            sys.stdout.write("Please respond with 'yes' or 'no' "
                             "(or 'y' or 'n').\n")


def migrate():
    # Migrate from devices.py to devices.json
    if not os.path.isfile(devices_filepath_old):
        print('Could not find {}, aborting'.format(devices_filepath_old))
        sys.exit(1)

    from devices import devices
    with open(devices_filename, 'w') as json_fh:
        json.dump({'devices': devices}, json_fh, indent=4)

    # Backup old file
    shutil.move(devices_filepath_old, devices_filepath_old_bak)

    print('Migrated from {} to {} with {} device(s)'.format(devices_filename_old, devices_filename, len(devices)))
    print('{} has been moved to {}'.format(devices_filename_old, devices_filename_old_bak))


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Receive alerts from munin and relay them to Google Cloud Messaging')
    parser.add_argument("--test", action="store_true", dest="test", default=False)
    parser.add_argument("--migrate", action="store_true", dest="migrate", default=False)
    parser.add_argument("--add-device", dest="add_device")
    args = parser.parse_args()

    if args.migrate:
        migrate()
    elif args.add_device is not None:
        devices = get_devices()
        reg_id = args.add_device

        if reg_id not in devices:
            devices.append(reg_id)

            with open(devices_filepath, 'w') as json_fh:
                json.dump({'devices': devices}, json_fh, indent=4)

            print('{} updated with {} device(s)'.format(devices_filename, len(devices)))
        else:
            print('{} already contains {}.'.format(devices_filename, reg_id))

        if ask_yes_no('Do you want to send a test notification to this device?'):
            do_test([reg_id])
    else:
        devices = get_devices()

        if devices is None or len(devices) == 0:
            print('{} is empty, aborting'.format(devices_filename))
            sys.exit(1)

        if args.test:
            do_test(devices)
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
