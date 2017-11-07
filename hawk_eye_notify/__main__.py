docstr = """hawk_eye_notify
Hawk_Eye_Notify will run a single script with as many xargs as are passed to it.
If the job being run requires multiple scripts, design one script to accept the args
needed to run the others and run that one.

One thing to note is that the script will be ran from the root path / so all xargs
taht represent paths need to be absolute

Ex:
hawk_eye_notify test_dir HEN_test log_emailer.py /vagrant-install/hawk_eye_notify/hawk_eye_notify.conf.yaml

Usage:
  hawk_eye_notify.py --version
  hawk_eye_notify.py [-hv] <watch_dir_path> <run_name> [-o <log_out_path>] <script> [<xargs> ...]

Arguments:
  <watch_dir_path>                                 Full path to directory being watched
  <run_name>                                       A unique name for this hawk_eye run
  <script>                                         Script to run

Options:
  -h --help                                        Show this screen.
  -v --version                                     Show version.
  -o <output_path> --output=<output_path>          Path to output log file
"""

from docopt import docopt
from hawk_eye_notify.version import __version__
import hawk_eye_notify.watcher as watcher

import os

def main(args):
    run_name = args['<run_name>']
    output_path = os.path.realpath(args['--output'] or (os.path.join(os.getcwd(), run_name + '.log')))
    watched_dir = os.path.realpath(args['<watch_dir_path>'])
    script = os.path.realpath(args['<script>'])
    xargs = args['<xargs>']

    watcher.new_created_watcher(watched_dir, run_name, output_path, script, xargs)

def cli_run():
    args = docopt(docstr, version = 'Hawk_Eye_Notify %s' % __version__)
    main(args)

if __name__ == '__main__':
    cli_run()
    exit()
