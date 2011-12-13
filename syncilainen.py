#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# syncilainen
# 
# Monitor a pre-configured directory for changes and then synch
# automatically to a pre-configured version control respository.
#
# Authors: Konrad Markus <konker@gmail.com>
#

import pathhack

import sys
import time
import signal
import os.path
import logging
import optparse
import threading

from lib import json
from watcher import EventWatcher, Event
from notifier import Notifier
from actions.vcs_action import Action

DEFAULT_CONF_FILE='syncilainen.json'
DEFAULT_LOG_FILE=None


class SyncilainenException(Exception): pass

class Syncilainen(object):
    def __init__(self, conf_file=DEFAULT_CONF_FILE):
        self.conf_file = conf_file
        self.watchers = []
        self.load_config()

    def start(self):
        for w in self.watchers:
            logging.info("Syncilainen.start: %s" % w)
            w.start()

    def stop(self):
        for w in self.watchers:
            logging.info("Syncilainen.stop: %s" % w)
            w.stop()
        self.watchers = []

    def reload_config(self):
        self.stop()
        self.load_config()
        self.start()

    def load_config(self):
        # read the configuration JSON file
        logging.info("Reading config: %s" % self.conf_file)
        config = None
        try:
            fp = open(self.conf_file)
            config = json.load(fp)
        except:
            logging.error(sys.exc_info()[1])
            exit(1)

        if config:
            # start
            for d in config['watch_directories']:
                # XXX: should str() be used here?
                watch_directory = str(os.path.abspath(os.path.expanduser(d['path'])))
                logging.info("watching: %s", d['path'])

                action = Action(watch_directory, d['auto_callback_secs'])
                if d['notifier']['enabled']:
                    action.notifier = Notifier('Syncilainen', d['notifier']['disable_after_n_errors'])
                self.watchers.append(EventWatcher(action))
        else:
            raise SyncilainenException("Could not load config file")


def read_options():
    # read in command line options
    parser = optparse.OptionParser()
    parser.add_option('-c', '--conf-file', dest='conf_file', default=DEFAULT_CONF_FILE, help="Config file location (defaults to %s)" % DEFAULT_CONF_FILE)
    parser.add_option('--log', dest='log_file', default=DEFAULT_LOG_FILE, help="where to send log messages (defaults to %s)" % DEFAULT_LOG_FILE)
    parser.add_option('--debug', dest='debug', action='store_true', default=False, help='Debug mode')
    
    options, args = parser.parse_args()
    if len(args) != 1:
        parser.error("Unknown arguments %s\n" % args)
    print(options)
    return options


def setup_logging(log_file=None, debug=False):
    # set up logging
    if log_file:
        filename = log_file
        stream = None
    else:
        filename = None
        stream = sys.stderr

    datefmt = '%Y-%m-%d %H:%M:%S'

    if debug:
        level=logging.DEBUG
        format='%(asctime)s [%(threadName)s] %(message)s'
    else:
        level=logging.INFO
        format='%(asctime)s %(message)s'

    if stream:
        logging.basicConfig(level=level,
                            format=format,
                            stream=stream,
                            datefmt=datefmt)
    else:
        logging.basicConfig(level=level,
                            format=format,
                            filename=filename,
                            datefmt=datefmt)

'''
        def pull_timer(secs):
            action.callback(Event({}))
            if secs > 0:
                t = threading.Timer(secs, pull_timer, [secs])
                t.start()

        # start pull timer
        #pull_timer(d['auto_pull_secs'])

    else:
        logging.error("Could not load config")
        exit(2)
'''
def main():
    syncilainen = None

    def reload(signum, stack):
        if syncilainen:
            syncilainen.reload_config()

    def quit(signum, stack):
        if syncilainen:
            syncilainen.stop()
        exit(0)

    # listen for SIGHUP or SIGUSR1 and reload config
    signal.signal(signal.SIGHUP, reload)
    signal.signal(signal.SIGUSR1, reload)

    # listen for SIGINT and quit gracefully
    signal.signal(signal.SIGINT, quit)

    # boilerplate
    options = read_options()
    setup_logging(options.log_file, options.debug)
    
    logging.info("PID: %s" % os.getpid())
    
    # start the syncilainen daemon
    syncilainen = Syncilainen()
    syncilainen.start()

    # wait for signals
    while True:
        signal.pause()


def init():
    options = read_options()
    setup_logging(options.log_file, options.debug)

    # start the syncilainen daemon
    syncilainen = Syncilainen(options.conf_file)
    syncilainen.start()


if __name__ == '__main__':
    main()


