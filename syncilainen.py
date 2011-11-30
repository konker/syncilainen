#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# syncilainen.py
# 
#
# Authors: Konrad Markus <konker@gmail.com>
#

import os.path
import logging
from watcher import EventWatcher
from notifier import Notifier
from actions.vcs_action import Action

def main(config):
    for d in config['watch_directories']:
        # XXX: should str() be used here?
        watch_directory = str(os.path.abspath(os.path.expanduser(d['path'])))
        logging.info("watching: %s", d['path'])

        # TODO: not really using conf properly
        action = Action(watch_directory)
        if d['notifier']['enabled']:
            action.notifier = Notifier('Syncilainen', d['notifier']['disable_after_n_errors'])
        watcher = EventWatcher(action)
        try:
            watcher.start()
        except KeyboardInterrupt:
            watcher.stop()


if __name__ == '__main__':
    import optparse
    import json
	 
    # read in command line options
    parser = optparse.OptionParser()
    parser.add_option('-c', '--conf-file', dest='conf_file', default='syncilainen.json', help='Config file location (defaults to hrm.conf)')
    parser.add_option('--debug', dest='debug', action='store_true', default=False, help='Debug mode')
    parser.add_option('--log', dest='logfile', help='where to send log messages')
    
    options, args = parser.parse_args()
    if len(args) != 0:
        parser.error("Unknown arguments %s\n" % args)

    # set up logging
    if not options.logfile:
        options.logfile = 'syncilainen.log'

    if options.debug:
        logging.basicConfig(level=logging.DEBUG,
                            filename=options.logfile,
                            format='%(asctime)s [%(threadName)s] %(message)s',
                            datefmt='%Y-%m-%d %H:%M:%S')
    else:
        logging.basicConfig(level=logging.INFO,
                            filename=options.logfile,
                            format='%(asctime)s %(message)s',
                            datefmt='%Y-%m-%d %H:%M:%S')
    
    # read the configuration JSON file
    config = None
    try:
        fp = open(options.conf_file)
        config = json.load(fp)
    except Exception as ex:
        logging.error(ex)
        exit(1)

    # start
    if config:
        main(config)
    else:
        exit(2)

