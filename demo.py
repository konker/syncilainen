import os.path
from datetime import datetime
from watcher import EventWatcher
from notifier import Notifier, NORMAL_LEVEL, ERROR_LEVEL
from vcs.git import VCS

WATCH_DIRECTORY = os.path.abspath('./sandbox')

vcs = VCS(WATCH_DIRECTORY)
notifier = Notifier('Syncilainen')

def vcs_commit_callback(event):
    if vcs.ignore_path in event.pathname:
        return

    out,error = vcs.pull()
    print("PULL")
    print(out, error)
    if 'conflict' in out:
        notifier.notify(out, ERROR_LEVEL)
        return
    elif 'Aborting' in out:
        notifier.notify(error, ERROR_LEVEL)

    status = vcs.status()
    if len(status) > 0:
        modes,files = zip(*status)
        message = "syncilainen: %s: %s" % (datetime.now().isoformat(), ','.join(files))

        vcs.add()

        out,error = vcs.commit(message)
        if not error == '':
            notifier.notify(error, ERROR_LEVEL)
            return

        out,error = vcs.push()
        print("PUSH")
        print(out, error)
        if '[rejected]' in out:
            notifier.notify(error, ERROR_LEVEL)

            out,error = vcs.pull()
            print("PULL")
            print(out, error)
            if 'conflict' in out:
                notifier.notify(out, ERROR_LEVEL)

            return

        # Everything went OK
        notifier.notify(message, NORMAL_LEVEL)

watcher = EventWatcher(['./sandbox'], vcs_commit_callback)
try:
    watcher.start()
except KeyboardInterrupt:
    watcher.stop()

