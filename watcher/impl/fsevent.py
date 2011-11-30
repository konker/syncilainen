import fsevents
import logging

class EventImpl(object):
    def __init__(self, rep):
        # 'cookie', 'mask', 'name'
        self.pathname = rep.name
        self.mask = rep.mask

    def __str__(self):
        return "fsevent.EventImpl: %s, %s" % (self.mask, self.pathname)


class EventWatcherImpl(object):
    def __init__(self, watch_directory, action):
        self.handler = EventHandlerImpl(action)

        self._observer = fsevents.Observer()
        self._stream = fsevents.Stream(self.handler, watch_directory, file_events=True)
        logging.info("Using fsevents watcher")

    def start(self):
        self._observer.schedule(self._stream)
        self._observer.start()

    def stop(self):
        self._observer.unschedule(self._stream)
        self._observer.stop()


class EventHandlerImpl(object):
    def __init__(self, action):
        self.action = action

    def __call__(self, event):
        self.action.callback(EventImpl(event))


