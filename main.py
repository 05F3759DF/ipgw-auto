#!/usr/bin/env python3

import argparse
import os
import sys
import time
import urllib.request
import getpass
import connect
import daemon

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='auto-connect')
    parser.add_argument('-p', '--pidfile', metavar='PIDFILE', type=str, default='/tmp/auto-connect.pid',
                        help='set the pid file.')
    parser.add_argument('-l', '--logfile', metavar='LOGFILE', type=str, default='/tmp/auto-connect.log',
                        help='set the log file.')
    parser.add_argument('-i', '--intervel', metavar='INTERVEL', type=int, default=1800,
                        help='set the intervel time.')
    parser.add_argument('-u', '--id', metavar='ID',
                        type=str, help='set the id.')
    parser.add_argument('-w', '--password', metavar='PASSWORD',
                        type=str, help='set the password.')
    parser.add_argument('-d', '--daemon', choices=['start', 'stop', 'restart'], nargs='?', const='start',
                        help='set if works in daemon mode.')
    args = parser.parse_args()

    if args.id:
        id = args.id
        if args.password:
            password = args.password
        else:
            password = getpass.getpass('Input your password:')
    else:
        id = input('Input your id:')
        password = getpass.getpass('Input your password:')

    if args.daemon:
        if args.daemon == 'start':
            try:
                daemon.daemonize(
                    args.pidfile, stderr=args.logfile, stdout=args.logfile)
            except RuntimeError as e:
                print(e, file=sys.stderr)
                raise SystemExit(1)
        elif args.daemon == 'stop':
            daemon.stop(args.pidfile)
            raise SystemExit(1)
        elif args.daemon == 'restart':
            daemon.stop(args.pidfile)
            try:
                daemon.daemonize(
                    args.pidfile, stderr=args.logfile, stdout=args.logfile)
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
            respense = urllib.request.urlopen(url, timeout=1)
            print(time.ctime(), 'all right')
        except Exception as e:
            print(time.ctime(), 'reconnect')
            try:
                connect.connect(id, password)
            except Exception as e:
                print(e)
        time.sleep(args.intervel)
