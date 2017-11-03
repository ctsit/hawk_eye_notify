import pyinotify
import os
import subprocess, sys

class EventHandler(pyinotify.ProcessEvent):
    def my_init(self, **kwargs):
        self.runnable_actions = kwargs.get('runnable_actions')
        self.config_path = kwargs.get('config_path')

    def process_IN_CREATE(self, event):
        print("New file detected: ", event.pathname)
        for script in self.runnable_actions:
            print("Running script: ", script)
            args = [sys.executable, script, os.path.abspath(event.pathname), self.config_path]
            print(args)
            subprocess.Popen(args, stderr=subprocess.STDOUT)
        print("Finished with new file")

def new_created_watcher(watched_dir, run_name, output_path, actions_list, config_path):
    """
    This function takes 4 arguments:
    -watched_dir: the directory being watched for changes
    -run_name: a unique name for this watching job
    -output_path: path for output logs
    -actions_list: a list of scripts to run when the action happens
    -config_path: abspath for the config file
    """
    wm = pyinotify.WatchManager()
    wm.add_watch(watched_dir, pyinotify.IN_CREATE, rec=True)

    handler = EventHandler(runnable_actions=actions_list, config_path = config_path)
    notifier = pyinotify.Notifier(wm,handler)

    try:
        notifier.loop(daemonize=True,  pid_file=os.path.join('/tmp', run_name + '.pid'), stdout=output_path)
    except pyinotify.NotifierError as err:
       print("error:", err)
