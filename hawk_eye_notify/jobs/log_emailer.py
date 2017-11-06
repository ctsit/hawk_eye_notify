#!/usr/bin/env python
import sys, os
import json
from templater import get_template
from emailer import send_email
from yaml_reader import get_config

# Required config fields:
_expected_fields = 'expected_fields'

def event_handler(full_event_path, config_file_path):
    log, success = read_in_log(full_event_path)
    log, success = validate_log(log, success, full_event_path, config_file_path)

    template = get_template(log,config_file_path)
    build_email(template, success, config_file_path)

def read_in_log(file_path):
    success = True
    log = None
    with open(file_path, 'r') as json_file:
        raw_log = json_file.read()
    try:
        log = json.loads(raw_log)
        print('JSON loaded in successfully')
    except Exception as err:
        print('JSON failed to load')
        log = generate_fail_log(raw_log, err)
        success = False

    return log, success

def validate_log(log, success, file_path, config_file_path):
    """
    Checks a properly formatted JSON object for all the required fields
    """
    expected_fields = get_config(config_file_path, _expected_fields)
    error = ''
    for field in expected_fields:
        if field not in log:
            error += 'Missing %s in log. ' % field
    if error:
        log = generate_fail_log(json.dumps(log, indent=4), error)
        print("Log failed: ", error)
        success = False

    log['file_path'] = file_path
    print('Log has been validated')
    print('Source: ', log['source'])
    return log, success

def generate_fail_log(output, error):
    return {'output': output, 'error': error, 'source': 'failed_v1'}

def build_email(template, success, config_file_path):
    #an email needs a host, port, subject, message, from, to, and maybe type (html/txt)
    if success:
        subject = 'Log has been successfully processed'
    else:
        subject = 'Log was unable to be processed'

    send_email(subject, template, config_file_path)
    print("Email sent\n")

if __name__ == '__main__':
    log_path = 1
    config_path = 2
    print(sys.executable)
    event_handler(sys.argv[log_path], sys.argv[config_path])
    exit()
