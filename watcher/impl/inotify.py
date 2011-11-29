import pyinotify


class EventImpl(object):
    def __init__(self, rep):
        # 'dir', 'mask', 'maskname', 'name', 'path', 'pathname', 'wd'
        self.pathname = rep.pathname
        self.mask = rep.mask

    def __str__(self):
        return "EventImpl: %s, %s" % (self.mask, self.pathname)


class EventWatcherImpl(object):
    def __init__(self, file_paths, callback):
        self.file_paths = file_paths
        self.handler = EventHandlerImpl(callback)

        mask = pyinotify.IN_ATTRIB
        mask |= pyinotify.IN_CREATE
        mask |= pyinotify.IN_DELETE
        mask |= pyinotify.IN_MODIFY
        mask |= pyinotify.IN_MOVED_FROM
        mask |= pyinotify.IN_MOVED_TO

        self.__wm = pyinotify.WatchManager()
        self.__notifier = pyinotify.Notifier(self.__wm, self.handler)
        wdd = self.__wm.add_watch(file_paths, mask, rec=True)

    def start(self):
        self.__notifier.loop()

    def stop(self):
        #[FIXME: something here?]
        pass


class EventHandlerImpl(pyinotify.ProcessEvent):
    def __init__(self, callback):
        self.callback = callback

    def process_default(self, event):
        self.callback(EventImpl(event))

