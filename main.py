import time
import sys
import os
import urllib.request


if __name__ == '__main__':
    sys.stderr = sys.stdout = open('connect.log', 'a', 1)
    if os.fork():
        exit()
    while True:
        url = 'http://www.baidu.com'
        try:
            respense = urllib.request.urlopen(url, timeout=1)
        except Exception as e:
            # print(str(e.reason) == 'timed out')
            if e.reason and str(e.reason) == 'timed out':
                print(time.ctime(), 'reconnect')
                os.system('./connect.sh connect domestic {0} {1}'.format('id', 'passwd')')
        time.sleep(3600)
