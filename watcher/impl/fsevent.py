# -*- coding: utf-8 -*-
#
# watcher.impl.fsevent
# 
# MacFSEvents implementation of the EventWatcher interface (Mac OS X)
#
# Authors: Konrad Markus <konker@gmail.com>
#

import fsevents
import logging


class EventImpl(object):
    def __init__(self, rep):
        # 'cookie', 'mask', 'name'
        if rep:
            self.pathname = rep.name
            self.mask = rep.mask
        else:
            self.pathname = ''
            self.mask = 0

    def __str__(self):
        return "fsevent.EventImpl: %s, %s" % (self.mask, self.pathname)


class EventWatcherImpl(object):
    def __init__(self, watch_directory, action):
        self.handler = EventHandlerImpl(action)

        self._observer = fsevents.Observer()
        self._stream = fsevents.Stream(self.handler, watch_directory, file_events=True)
        logging.info("Using EventWatcher: fsevents")

    def start(self):
        logging.info("Starting: %s" % self)
        self._observer.schedule(self._stream)
        self._observer.start()

    def stop(self):
        logging.info("Stopping: %s" % self)
        self._observer.unschedule(self._stream)
        self._observer.stop()


class EventHandlerImpl(object):
    def __init__(self, action):
        self.action = action

    def __call__(self, event):
        self.action.callback(EventImpl(event))


