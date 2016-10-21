#!/usr/bin/env python3
import urllib.request
import re
import argparse
import getpass


def connect(username, password, *, irange='2', action='connect'):
    url = 'https://its.pku.edu.cn:5428/ipgatewayofpku?uid={username}&password={password}&range={irange}&operation={action}&timeout=1' \
        .format(username=username, password=password, irange=irange, action=action)
    # print(url)
    response = urllib.request.urlopen(url, timeout=1)
    data = response.read().decode('GB18030')
    # print(data)
    g = re.search('IPGWCLIENT_START (.*) IPGWCLIENT_END', data)
    msg = g.group(1)
    return msg


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='auto-connect')
    parser.add_argument('-u', '--id', metavar='ID', type=str, help='set the id.')
    parser.add_argument('-w', '--password', metavar='PASSWORD', type=str, help='set the password.')
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

    ret = connect(id, password)
    print(ret)
