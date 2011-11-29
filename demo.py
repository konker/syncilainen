import os.path
from datetime import datetime

from watcher import EventWatcher
from notifier import Notifier, NORMAL_LEVEL, ERROR_LEVEL
from vcs import VCS


WATCH_DIRECTORY = os.path.abspath('./sandbox')

vcs = VCS(WATCH_DIRECTORY)
notifier = Notifier('Syncilainen')

def vcs_commit_callback(event):
    if vcs.ignore_path in event.pathname:
        return

    ok,error = vcs.pull()
    if not ok:
        notifier.notify(error, ERROR_LEVEL)
        return

    status = vcs.status()
    if len(status) > 0:
        modes,files = zip(*status)
        message = "syncilainen: %s: %s" % (datetime.now().isoformat(), ','.join(files))

        ok,error = vcs.commit_all(message)
        if not ok:
            notifier.notify(error, ERROR_LEVEL)
            return

        ok,error = vcs.push()
        if not ok:
            notifier.notify(error, ERROR_LEVEL)

            # Do another pull to auto-merge in conflicts if any
            ok,error = vcs.pull()
            if not ok:
                notifier.notify(error, ERROR_LEVEL)

            return

        # Everything went OK
        notifier.notify(message, NORMAL_LEVEL)

watcher = EventWatcher(['./sandbox'], vcs_commit_callback)
try:
    watcher.start()
except KeyboardInterrupt:
    watcher.stop()

