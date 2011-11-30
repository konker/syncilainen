# -*- coding: utf-8 -*-
#
# actions.vcs_actions
# 
# Commit to a remote VCS repository on filesystem events
#
# Authors: Konrad Markus <konker@gmail.com>
#

import logging
from datetime import datetime
from vcs import VCS
from notifier import NORMAL_LEVEL, ERROR_LEVEL

class Action(object):
    def __init__(self, watch_directory, notifier=None):
        self.watch_directory = watch_directory
        self.notifier = notifier
        self.vcs = VCS(watch_directory)
        logging.info("Using Action: vcs")

    def callback(self, event):
        if self.vcs.ignore_path in event.pathname:
            logging.debug("ignoring: %s" % event.pathname)
            return

        logging.debug("%s: pull" % event.pathname)
        ok,error = self.vcs.pull()
        if not ok:
            logging.error("%s: pull" % error)
            if self.notifier:
                self.notifier.notify(error, ERROR_LEVEL)
            return

        status = self.vcs.status()
        if len(status) > 0:
            modes,files = zip(*status)
            message = "syncilainen: %s: %s" % (datetime.now().isoformat(), ','.join(files))

            logging.debug("%s: add" % event.pathname)
            ok,error = self.vcs.add()
            if not ok:
                logging.error("%s: add" % error)
                if self.notifier:
                    self.notifier.notify(error, ERROR_LEVEL)
                return

            logging.debug("%s: commit_all" % event.pathname)
            ok,error = self.vcs.commit_all(message)
            if not ok:
                logging.error("%s: commit_all" % error)
                if self.notifier:
                    self.notifier.notify(error, ERROR_LEVEL)
                return

            logging.info("%s: push" % event.pathname)
            ok,error = self.vcs.push()
            if not ok:
                logging.error("%s: push" % error)
                if self.notifier:
                    self.notifier.notify(error, ERROR_LEVEL)

                return

            # Everything went OK
            logging.info("%s: OK: %s" % (event.pathname, message))
            if self.notifier:
                self.notifier.notify(message, NORMAL_LEVEL)

