import time
import os
import urllib2

triggerfile = '/home/cotton-admin/gunicorn_stackdumps/dump-stack-traces.txt'

def sigdump(code='', exc=''):
    f = open(triggerfile, 'a')
    f.write('time:%s|code:%s|exception:%s\n' % (time.strftime('%Y-%m-%d %H:%M:%S'), code, exc))
    f.close()

while 1:
    handle = None
    try:
        response = urllib2.urlopen('http://shop.cottonon.com.au')
    except Exception, e:
        sigdump(exc=e)
    else:
        if response.code != 200:
            sigdump(code=response.code)

    time.sleep(5)
