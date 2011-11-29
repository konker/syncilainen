
class UnknownAPIException(Exception): pass

try:
    from impl.growlnotify import NotifierImpl
except ImportError:
    try:
        from impl.notifysend import NotifierImpl
    except ImportError:
        from impl.dummy import NotifierImpl


def Notifier(title):
    return NotifierImpl(title)

