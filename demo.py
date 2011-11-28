from watcher import EventWatcher

def cb(event):
    print(event.pathname)

watcher = EventWatcher(['.'], cb)
try:
    watcher.start()
except KeyboardInterrupt:
    watcher.stop()

