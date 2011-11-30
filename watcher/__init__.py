# -*- coding: utf-8 -*-
#
# watcher
# 
# Dynamically loads a EventWatcher interface implementation
#
# Authors: Konrad Markus <konker@gmail.com>
#

class UnknownWatcherException(Exception): pass

try:
    from impl.fsevent import EventWatcherImpl, EventImpl
except ImportError:
    try:
        from impl.inotify import EventWatcherImpl, EventImpl
    except ImportError:
        raise UnknownWatcherException()


def Event(event):
    return EventImpl(event)

def EventWatcher(action):
    return EventWatcherImpl(action.watch_directory, action)

