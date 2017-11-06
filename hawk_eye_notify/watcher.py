import pyinotify
import os
import subprocess, sys

class EventHandler(pyinotify.ProcessEvent):
    def my_init(self, **kwargs):
        self.runnable_script = kwargs.get('runnable_script')
        self.xargs = kwargs.get('xargs')

    def process_IN_CREATE(self, event):
        print("New file detected: ", event.pathname)
        print("Running script: ", self.runnable_script)
        args = [self.runnable_script, os.path.abspath(event.pathname)]
        args.extend(self.xargs)
        print("Like: ", args)
        subprocess.Popen(args, stderr=subprocess.STDOUT)
        print("Finished with new file")

def new_created_watcher(watched_dir, run_name, output_path, script, script_xargs):
    """
    This function takes 4 arguments:
    -watched_dir: the directory being watched for changes
    -run_name: a unique name for this watching job
    -output_path: path for output logs
    -script: a script to run when the action happens
    -script_xargs: a list of any extra args the script will need to run
    """
    wm = pyinotify.WatchManager()
    wm.add_watch(watched_dir, pyinotify.IN_CREATE, rec=True)

    handler = EventHandler(runnable_script=script, xargs=script_xargs)
    notifier = pyinotify.Notifier(wm,handler)

    try:
        notifier.loop(daemonize=True,  pid_file=os.path.join('/tmp', run_name + '.pid'), stdout=output_path)
    except pyinotify.NotifierError as err:
        print("error:", err)
