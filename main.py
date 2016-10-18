#!/usr/bin/env python3

import time
import sys
import os
import signal
import argparse
import urllib.request
import daemon

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='auto-connect')
    parser.add_argument('-p', '--pidfile', metavar='PIDFILE', type=str, default='/tmp/auto-connect.pid', help='set the pid file.')
    parser.add_argument('-l', '--logfile', metavar='LOGFILE', type=str, default='/tmp/auto-connect.log', help='set the log file.')
    parser.add_argument('-d', '--daemon', choices=['start', 'stop', 'restart'], nargs='?', const='start', help='set if works in daemon mode.')
    args = parser.parse_args()
    if args.daemon:
        if args.daemon == 'start':
            try:
                daemon.daemonize(args.pidfile, stderr=args.logfile, stdout=args.logfile)
            except RuntimeError as e:
                print(e, file=sys.stderr)
                raise SystemExit(1)
        elif args.daemon == 'stop':
            daemon.stop(args.pidfile)
            raise SystemExit(1)
        elif args.daemon == 'restart':
            daemon.stop(args.pidfile)
            try:
                daemon.daemonize(args.pidfile, stderr=args.logfile, stdout=args.logfile)
            except RuntimeError as e:
                print(e, file=sys.stderr)
                raise SystemExit(1)
        else:
            print('Unknown command {!r}'.format(sys.argv[1]), file=sys.stderr)
            raise SystemExit(1)
    else:
        if os.path.exists(args.pidfile):
            raise RuntimeError('Already running')

    while True:
        url = 'http://www.baidu.com'
        try:
            respense = urllib.request.urlopen(url, timeout=10)
            print(time.ctime(), 'all right')
        except Exception as e:
            # print(str(e.reason) == 'timed out')
            if e.reason and str(e.reason) == 'timed out':
                print(time.ctime(), 'reconnect')
                try:
                    os.system('~/connect.sh connect domestic {0} {1}'.format('id', 'passwd'))
                except Exception as e:
                    print(e)
        time.sleep(3600)
