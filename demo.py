import os.path
from watcher import EventWatcher
from notifier import Notifier
from actions.vcs_action import Action


WATCH_DIRECTORY = os.path.abspath('./sandbox')

action = Action(WATCH_DIRECTORY)
action.notifier = Notifier('Syncilainen')
watcher = EventWatcher(action)
try:
    watcher.start()
except KeyboardInterrupt:
    watcher.stop()

