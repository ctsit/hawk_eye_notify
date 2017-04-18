VER= '1.0.0'
docstr = """hawk_eye_notify

Usage:
  hawk_eye_notify.py --version
  hawk_eye_notify.py <watch_dir_path> [--conf=<conf_file>] [--rec]

Arguments:
  <watch_dir_path>                    Full path to directory being watched

Options:
  -h --help                           Show this screen.
  -v --version                        Show version.
  -r --rec                            Recursively add watches on all directories
  -c=<conf_file> --conf=<conf_file>   Config file path
                                      [default: hawk_eye_notify.conf.yaml]
"""

import json

from docopt import docopt
import pyinotify
from templater import Templater
from send_email import send_email
import yaml
import sys
import os

_map_conf = 'product_template_map'
_fail_template = 'failed_v1'

class EventHandler(pyinotify.ProcessEvent):
    def my_init(self, **kargs):
        self.local_path = kargs['local_path']
        self.templater = Templater(self.local_path)

    def process_IN_CREATE(self, event):
        #event.pathname has a leading /, linux thinks it's absolute
        full_event_path = self.local_path + event.pathname

        print("New file: ", full_event_path)
        log, success = read_log(full_event_path)
        if success:
            print("File moved to completed")
            move_to_dir(full_event_path, os.path.join(self.local_path, completed_path))
        else:
            print("File moved to failed")
            move_to_dir(full_event_path, os.path.join(self.local_path, failed_path))

        template = build_template(self.templater, log, success)
        build_email(template, success)

def main(args=docopt(docstr)):
    local_path = sys.path[0]
    wm = pyinotify.WatchManager()
    handler = EventHandler(local_path=local_path)
    notifier = pyinotify.Notifier(wm,handler)

    global configs
    configs = __read_config(args['--conf'])
    __make_processed_dirs(args['<watch_dir_path>'])
    wm.add_watch(args['<watch_dir_path>'], pyinotify.IN_CREATE, rec=True)
    try:
        notifier.loop(daemonize=True, pid_file=os.path.join(local_path, 'hawk_eye_notify.pid'),
                      stdout=os.path.join(local_path, 'hawk_eye_notify.log'))
    except pyinotify.NotifierError as err:
       print("error:", err)

def __read_config(config_file_path):
    """
    Read in a YAML config file
    """
    config = None
    with open(config_file_path, 'r') as config_file:
        try:
           config = yaml.load(config_file.read())
        except yaml.YAMLError as exc:
            print(exc)

    return config

def __make_processed_dirs(path):
    global completed_path
    global failed_path
    completed_path = os.path.join(path, 'completed')
    failed_path = os.path.join(path, 'failed')

    if not os.path.exists(completed_path):
        os.makedirs(completed_path, exist_ok=True)

    if not os.path.exists(failed_path):
        os.makedirs(failed_path, exist_ok=True)

def move_to_dir(file_to_move, move_to_dir):
    """Simply move a file to a new directory"""

    file_name = os.path.basename(file_to_move)
    move_to_path = os.path.join(move_to_dir, file_name)
    os.rename(file_to_move, move_to_path)

def read_log(file_path):
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

    return validate_log(log, success, file_path)

def validate_log(log, success, file_path):
    """
    Checks a properly formatted JSON object for all the required fields
    """
    error = ''
    for field in configs['expected_fields']:
        if field not in log:
            error += 'Missing %s in log. ' % field
    if error:
        log = generate_fail_log(json.dumps(log, indent=4), error)
        success = False

    log['file_path'] = file_path
    print('Log has been validated')
    print('Source: ', log['source'])
    return log, success

def generate_fail_log(output, error, template=_fail_template):
    return {'output': output, 'error': error, 'source': template}

def build_template(templater, log, success=True):
    if success:
        source = log.get('source', _fail_template)
    else:
        source = _fail_template

    template_name = get_template_name(source)
    print("Template name: ", template_name)
    template = templater.get_template(template_name, log)
    return template

def get_template_name(source):
    #magic ints
    src = 0
    ver = 1

    #source is in name_version format
    source_ver = source.split('_')
    template_name = configs[_map_conf].get(source_ver[src], {}).get(source_ver[ver], None)
    return template_name

def build_email(template, success=True):
    #an email needs a host, port, subject, message, from, to, and maybe type (html/txt)
    email_settings = configs['email_settings']
    if success:
        subject = 'Log has been successfully processed'
    else:
        subject = 'Log was unable to be processed'

    send_email(subject, template, email_settings)

    print("Email sent\n")

if __name__ == '__main__':
    arguments = docopt(docstr, version=VER)
    main(arguments)
