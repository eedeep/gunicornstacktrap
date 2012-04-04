import time
import os
import urllib2
import subprocess

diagnostic_commands = [
    ('ifconfig', ['ifconfig']),
    ('netstat', ['netstat', '-na']),
    ('lsof', ['lsof']),
    ('queries', ['mysql', '-uroot', '-proot', '-eshow full processlist;']),
    ('traceroute', ['traceroute', 'db.mysite.com.au']),
]

triggerfile = '/home/eedeep/gunicorn_stackdumps/dump-stack-traces.txt'

def sigdump(code='', exc=''):
    timestamp = time.strftime('%Y_%m_%d_%H_%M_%S')
    f = open(triggerfile, 'a')
    f.write('time:%s|code:%s|exception:%s\n' % (timestamp, code, exc))
    f.close()

    for cmd in diagnostic_commands:
        filename = '/home/peedee/gunicorn_stackdumps/%s_%s.txt' % (timestamp, cmd[0])
        output = subprocess.Popen(cmd[1], stdout=subprocess.PIPE).communicate()[0]
        f = open(filename, 'a')
        f.write(output)
        f.close()

while 1:
    handle = None
    try:
        response = urllib2.urlopen('http://mysite.com.au')
    except Exception, e:
        sigdump(exc=e)
    else:
        if response.code != 200:
            sigdump(code=response.code)

    time.sleep(5)
