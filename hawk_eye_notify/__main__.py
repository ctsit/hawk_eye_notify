docstr = """hawk_eye_notify

Usage:
  hawk_eye_notify.py --version
  hawk_eye_notify.py [-hv] <watch_dir_path> <run_name> <action_scripts>...
  hawk_eye_notify.py [-hv] <watch_dir_path> <run_name> <action_scripts>...  [-c <conf_file>] [-o <output_path>]

Arguments:
  <watch_dir_path>                                 Full path to directory being watched
  <run_name>                                       A unique name for this hawk_eye run

Options:
  -h --help                                        Show this screen.
  -v --version                                     Show version.
  -o <output_path> --output=<output_path>          Path to output log file
  -c=<conf_file> --conf=<conf_file>                Config file path
                                                   [default: hawk_eye_notify.conf.yaml]
"""

from docopt import docopt
from hawk_eye_notify.version import __version__
import hawk_eye_notify.watcher as watcher

import sys
import os

_map_conf = 'product_template_map'
_fail_template = 'failed_v1'

def main(args):
    run_name = args['<run_name>']
    output_path = os.path.realpath(args['--output'] or (os.path.join(os.getcwd(), run_name + '.log')))
    watched_dir = os.path.realpath(args['<watch_dir_path>'])
    scripts = [os.path.realpath(path) for path in args['<action_scripts>']]
    config_path = os.path.realpath(args['--conf'])

    watcher.new_created_watcher(watched_dir,run_name, output_path, scripts, config_path)

def cli_run():
    args = docopt(docstr, version = 'Hawk_Eye_Notify %s' % __version__)
    main(args)

if __name__ == '__main__':
    cli_run()
    exit()
