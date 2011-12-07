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
from vcs import VCS, OK
from notifier import NORMAL_LEVEL, ERROR_LEVEL

class Action(object):
    def __init__(self, id, watch_directory, notifier=None):
        self.id = id
        self.watch_directory = watch_directory
        self.notifier = notifier
        self.vcs = VCS(watch_directory)
        self._working = False
        logging.info("Using Action: vcs")

    def _add_commit_push_cycle(self, event):
        status = self.vcs.status()
        if len(status) > 0:
            modes,files = zip(*status)

            file_list = ','.join(files)
            message = "syncilainen[%s]: %s: %s" % aself.id, (datetime.now().isoformat(), file_list)

            logging.debug("%s: add" % event.pathname)
            result,error = self.vcs.add()
            if not result == OK:
                logging.error("%s: add" % error)
                if self.notifier:
                    self.notifier.notify(error, ERROR_LEVEL)
                return result,error

            logging.debug("%s: commit_all" % event.pathname)
            result,error = self.vcs.commit_all(message)
            if not result == OK:
                return result,error

            logging.debug("%s: push" % event.pathname)
            result,error = self.vcs.push()
            if not result == OK:
                # fetch
                logging.debug("%s: fetch" % event.pathname)
                result,error = self.vcs.fetch()

                # merge
                logging.debug("%s: merge" % event.pathname)
                result,error = self.vcs.merge()
                if not result == OK:
                    # ls_files
                    logging.debug("%s: get_unmerged" % event.pathname)
                    unmerged = self.vcs.get_unmerged()
                    logging.debug("unmerged: %s" % unmerged)

                    for u in unmerged:
                        # save theirs as <id>.<sha1>.<filename>
                        logging.debug("%s: save_theirs" % event.pathname)
                        self.vcs.save_theirs(u, id)

                        # force ours to be <filename>
                        logging.debug("%s: force_ours" % event.pathname)
                        self.vcs.force_ours(u)

                    # recurse
                    logging.debug("%s: recurse" % event.pathname)
                    return self._add_commit_push_cycle(event)

            # Everything went OK
            return result,message

        # Nothing to do
        return OK,""

    def callback(self, event):
        if self.vcs.ignore_path in event.pathname:
            #logging.debug("ignoring: %s" % event.pathname)
            return

        if self._working:
            #logging.debug("working.. ignoring: %s" % event.pathname)
            return

        self._working = True

        logging.debug("%s: _add_commit_push_cycle" % event.pathname)
        result,message = self._add_commit_push_cycle(event)
        if not result == OK:
            logging.error("%s: _add_commit_push_cycle" % error)
            if self.notifier:
                self.notifier.notify(error, ERROR_LEVEL)
        else:
            # Everything went OK
            logging.info("%s: OK: %s" % (event.pathname, message))
            self._working = False
            if self.notifier:
                self.notifier.notify(message, NORMAL_LEVEL)

