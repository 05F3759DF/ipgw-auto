#!/usr/bin/env python3
import urllib.request
import re
def connect(username, password, *,  irange='2', action='connect'):
	url = 'https://its.pku.edu.cn:5428/ipgatewayofpku?uid={username}&password={password}&range={irange}&operation={action}&timeout=1'\
	.format(username=username, password=password, irange=irange, action=action)
	print(url)
	response = urllib.request.urlopen(url)
	data = response.read().decode('GB18030')
	print(data)
	g = re.search('IPGWCLIENT_START (.*) IPGWCLIENT_END', data)
	msg = g.group(1)
	return msg

if __name__ == '__main__':
	username = '1601214567'
	password = '*'
	ret = connect(username, password)
	print(ret)

