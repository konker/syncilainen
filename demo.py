import os.path
from watcher import EventWatcher
from notifier import Notifier
from actions.vcs_action import Action


WATCH_DIRECTORY = os.path.abspath('./sandbox')

notifier = Notifier('Syncilainen')
action = Action(WATCH_DIRECTORY, notifier)
watcher = EventWatcher([WATCH_DIRECTORY], action)
try:
    watcher.start()
except KeyboardInterrupt:
    watcher.stop()

