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
import os.path
import logging
import optparse
import threading

from lib import json
from watcher import EventWatcher, Event
from notifier import Notifier
from actions.vcs_action import Action

def main(logfile=None, conf_file='syncilainen.json', debug=False):
    # read in command line options
    parser = optparse.OptionParser()
    parser.add_option('-c', '--conf-file', dest='conf_file', default=conf_file, help="Config file location (defaults to %s)" % conf_file)
    parser.add_option('--debug', dest='debug', action='store_true', default=debug, help='Debug mode')
    parser.add_option('--log', dest='logfile', default=logfile, help='where to send log messages')
    
    options, args = parser.parse_args()
    if len(args) != 0:
        parser.error("Unknown arguments %s\n" % args)

    # set up logging
    if options.logfile:
        filename = options.logfile
        stream = None
    else:
        filename = None
        stream = sys.stderr

    datefmt = '%Y-%m-%d %H:%M:%S'

    if options.debug:
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
    
    # read the configuration JSON file
    config = None
    try:
        fp = open(options.conf_file)
        config = json.load(fp)
    except:
        logging.error(sys.exc_info()[1])
        exit(1)

    if config:
        id = config['id']
        for d in config['watch_directories']:
            # XXX: should str() be used here?
            watch_directory = str(os.path.abspath(os.path.expanduser(d['path'])))
            logging.info("%s watching: %s", config['id'], d['path'])

            action = Action(config['id'], watch_directory)
            if d['notifier']['enabled']:
                action.notifier = Notifier('Syncilainen', d['notifier']['disable_after_n_errors'])
            watcher = EventWatcher(action)
            try:
                watcher.start()
            except KeyboardInterrupt:
                watcher.stop()
    else:
        logging.error("Could not load config")
        exit(2)


if __name__ == '__main__':
    try:
	    main()
    except KeyboardInterrupt:
        logging.info("Interrupted, exiting")
        exit(0)

