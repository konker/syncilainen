from datetime import datetime
from vcs import VCS
from notifier import NORMAL_LEVEL, ERROR_LEVEL

class Action(object):
    def __init__(self, watch_directory, notifier=None):
        self.watch_directory = watch_directory
        self.notifier = notifier
        self.vcs = VCS(watch_directory)

    def callback(self, event):
        if self.vcs.ignore_path in event.pathname:
            return

        ok,error = self.vcs.pull()
        if not ok:
            if self.notifier:
                self.notifier.notify(error, ERROR_LEVEL)
            return

        status = self.vcs.status()
        if len(status) > 0:
            modes,files = zip(*status)
            message = "syncilainen: %s: %s" % (datetime.now().isoformat(), ','.join(files))

            ok,error = self.vcs.commit_all(message)
            if not ok:
                if self.notifier:
                    self.notifier.notify(error, ERROR_LEVEL)
                return

            ok,error = self.vcs.push()
            if not ok:
                if self.notifier:
                    self.notifier.notify(error, ERROR_LEVEL)

                return

            # Everything went OK
            if self.notifier:
                self.notifier.notify(message, NORMAL_LEVEL)

