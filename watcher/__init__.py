
class UnknownAPIException(Exception): pass

try:
    from impl.fsevent import EventWatcherImpl, EventImpl
except ImportError:
    try:
        from impl.inotify import EventWatcherImpl, EventImpl
    except ImportError:
        raise UnknownAPIException()


def EventWatcher(action):
    return EventWatcherImpl(action.watch_directory, action)

