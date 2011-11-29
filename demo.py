from datetime import datetime
from watcher import EventWatcher
from vcs.git import VCS

vcs = VCS('./sandbox')

def cb(event):
    status = vcs.status()
    if len(status) > 0:
        modes,files = zip(*status)
        message = "syncilainen: %s: %s" % (datetime.now().isoformat(), ','.join(files))

        print(message)
        vcs.pull('origin')
        vcs.add('.')
        vcs.commit(message)
        vcs.push('origin')

watcher = EventWatcher(['./sandbox'], cb)
try:
    watcher.start()
except KeyboardInterrupt:
    watcher.stop()


