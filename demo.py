from datetime import datetime
from watcher import EventWatcher
from notifier import Notifier
from vcs.git import VCS

vcs = VCS('./sandbox')
notifier = Notifier('Syncilainen')

def vcs_commit_callback(event):
    vcs.pull()

    status = vcs.status()
    if len(status) > 0:
        modes, files = zip(*status)
        message = "syncilainen: %s: %s" % (datetime.now().isoformat(), ','.join(files))

        vcs.commit_and_push(message)

        notifier.notify(message)

watcher = EventWatcher(['./sandbox'], vcs_commit_callback)
try:
    watcher.start()
except KeyboardInterrupt:
    watcher.stop()

