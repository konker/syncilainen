import os.path
from datetime import datetime
from watcher import EventWatcher
from notifier import Notifier
from vcs.git import VCS

WATCH_DIRECTORY = os.path.abspath('./sandbox')

vcs = VCS(WATCH_DIRECTORY)
notifier = Notifier('Syncilainen')

def vcs_commit_callback(event):
    if vcs.ignore_path in event.pathname:
        return

    print(vcs.pull())

    status = vcs.status()
    if len(status) > 0:
        modes,files = zip(*status)
        message = "syncilainen: %s: %s" % (datetime.now().isoformat(), ','.join(files))

        print(vcs.add())
        print(vcs.commit(message))
        print(vcs.push())
        #vcs.commit_and_push(message)

        notifier.notify(message)

watcher = EventWatcher(['./sandbox'], vcs_commit_callback)
try:
    watcher.start()
except KeyboardInterrupt:
    watcher.stop()

