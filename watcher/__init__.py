
class UnknownAPIException(Exception): pass

try:
    from impl.fsevent import EventWatcherImpl, EventImpl
except ImportError:
    try:
        from impl.inotify import EventWatcherImpl, EventImpl
    except ImportError:
        raise UnknownAPIException()


def EventWatcher(file_paths, callback):
    return EventWatcherImpl(file_paths, callback)

