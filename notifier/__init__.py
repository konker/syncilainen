# -*- coding: utf-8 -*-
#
# notifier
# 
# Dynamically loads a Notifier interface implementation
#
# Authors: Konrad Markus <konker@gmail.com>
#

try:
    from impl.growlnotify import NotifierImpl, NORMAL_LEVEL_IMPL, ERROR_LEVEL_IMPL
except ImportError:
    try:
        from impl.notifysend import NotifierImpl, NORMAL_LEVEL_IMPL, ERROR_LEVEL_IMPL
    except ImportError:
        from impl.dummy import NotifierImpl, NORMAL_LEVEL_IMPL, ERROR_LEVEL_IMPL

NORMAL_LEVEL = NORMAL_LEVEL_IMPL
ERROR_LEVEL = ERROR_LEVEL_IMPL

def Notifier(title, disable_after_n_errors=-1):
    return NotifierImpl(title, disable_after_n_errors)

