# -*- coding: utf-8 -*-
#
# watcher.impl.inotify
# 
# pyinotify implementation of the EventWatcher interface (Linux)
#
# Authors: Konrad Markus <konker@gmail.com>
#

import pyinotify
import logging


class EventImpl(object):
    def __init__(self, rep):
        # 'dir', 'mask', 'maskname', 'name', 'path', 'pathname', 'wd'
        if rep:
            self.pathname = rep.pathname
            self.mask = rep.mask
        else:
            self.pathname = ''
            self.mask = 0

    def __str__(self):
        return "inotify.EventImpl: %s, %s" % (self.mask, self.pathname)


class EventWatcherImpl(object):
    def __init__(self, watch_directory, action):
        self.handler = EventHandlerImpl(action)

        mask = pyinotify.IN_ATTRIB
        mask |= pyinotify.IN_CREATE
        mask |= pyinotify.IN_DELETE
        mask |= pyinotify.IN_MODIFY
        mask |= pyinotify.IN_MOVED_FROM
        mask |= pyinotify.IN_MOVED_TO

        self.__wm = pyinotify.WatchManager()
        self.__notifier = pyinotify.Notifier(self.__wm, self.handler)
        self.__wm.add_watch([watch_directory], mask, rec=True)
        logging.info("Using EventWatcher: inotify")

    def start(self):
        self.__notifier.loop()

    def stop(self):
        #[FIXME: something here?]
        pass


class EventHandlerImpl(pyinotify.ProcessEvent):
    def __init__(self, action):
        self.action = action

    def process_default(self, event):
        self.action.callback(EventImpl(event))

