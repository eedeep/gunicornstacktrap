#!/usr/bin/python2.5

# Test server

import os

bind = "127.0.0.1:8002"
daemon = True
#daemon = False
debug = False
pidfile = "gunicorn.pid"
LOGFILE = logfile = "/var/www/sites/cottonon-staging/gunicorn.log"
workers = (os.sysconf("SC_NPROCESSORS_ONLN") * 4) + 1
loglevel = "debug"
timeout = 120

import os
import sys
import time
import signal
import threading
import atexit
import Queue
import traceback 

FILE = '/home/cotton-admin/gunicorn_stackdumps/dump-stack-traces.txt'

_interval = 1.0

_running = False
_queue = Queue.Queue()
_lock = threading.Lock()

def _stacktraces(): 
    code = [] 
    for threadId, stack in sys._current_frames().items(): 
        code.append("\n# ProcessId: %s" % os.getpid()) 
        code.append("# ThreadID: %s" % threadId) 
        for filename, lineno, name, line in traceback.extract_stack(stack): 
            code.append('File: "%s", line %d, in %s' % (filename, 
                    lineno, name)) 
            if line: 
                code.append("  %s" % (line.strip())) 

        filename = '/home/cotton-admin/gunicorn_stackdumps/%s_pid%s.txt' % (time.strftime('%Y_%m_%d_%H_%M_%S'), os.getpid())
        f = open(filename, 'a')
        for line in code:
            print >> sys.stderr, line
            f.write("%s\n" % line)
        f.close()
        
    sys.stderr.flush()

try:
    mtime = os.path.getmtime(FILE)
except:
    mtime = None

def _monitor():
    while 1:
        global mtime

        try:
            current = os.path.getmtime(FILE)
        except:
            current = None

        if current != mtime:
            mtime = current
            _stacktraces()

        # Go to sleep for specified interval.

        try:
            return _queue.get(timeout=_interval)
        except:
            pass

_thread = threading.Thread(target=_monitor)
_thread.setDaemon(True)

def _exiting():
    try:
        _queue.put(True)
    except:
        pass
    _thread.join()

atexit.register(_exiting)

def _start(interval=1.0):
    global _interval
    if interval < _interval:
        _interval = interval

    global _running
    _lock.acquire()
    if not _running:
        prefix = 'monitor (pid=%d):' % os.getpid()
        print >> sys.stderr, '%s Starting stack trace monitor.' % prefix
        _running = True
        _thread.start()
    _lock.release()

def post_fork(server, worker):
    _start()
