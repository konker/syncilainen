from watcher import EventWatcher
from vcs.git import VCS

vcs = VCS('.')

def cb(event):
    print(vcs.status())

watcher = EventWatcher(['.'], cb)
try:
    watcher.start()
except KeyboardInterrupt:
    watcher.stop()


