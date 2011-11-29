import fsevents


class EventImpl(object):
    def __init__(self, rep):
        # 'cookie', 'mask', 'name'
        self.pathname = rep.name
        self.mask = rep.mask

    def __str__(self):
        return "fsevent.EventImpl: %s, %s" % (self.mask, self.pathname)


class EventWatcherImpl(object):
    def __init__(self, file_paths, action):
        self.handler = EventHandlerImpl(action)

        self.__observer = fsevents.Observer()
        for f in file_paths:
            stream = fsevents.Stream(self.handler, f, file_events=True)
            self.__observer.schedule(stream)

    def start(self):
        self.__observer.start()

    def stop(self):
        self.__observer.stop()


class EventHandlerImpl(object):
    def __init__(self, action):
        self.action = action

    def __call__(self, event):
        self.action.callback(EventImpl(event))


