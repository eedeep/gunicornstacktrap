You can use this sketchy jerry rigged monitoring solution when you are having problems in production with gunicorn threads never returning and timing out.

You need to put the monitor code in your gunicorn.conf.py file.

Then you need to run the monitor which checks your production site to try to detect when the intermittent fault occurs (ie, the site returns something other than a 200):

nohup python monitorsite.py &

That script, when it gets back anything other than a 200, will write a new line to the file (ie, dump-stack-traces.log) which the stack dump monitor polls. 
When the stack dump monitor detects that that file has been touched, it will dump out stack traces for all running gunicorn threads to files which are named
with a timestamp and the process ID of the thread. Hopefully one of these files will contain the smoking gun.

Finally you can put this in crontab to get email alerts when something new gets written to the dump-stack-traces.log:

*/1 * * * *     perl /home/eedeep/gunicorn_stackdumps/tail_n_mail  --mailcom=/usr/sbin/sendmail /home/eedeep/gunicorn_stackdumps/stackmon_mail.config.cfg

Which will email you when anything new gets written to dump-stack-traces.log, so you know when to go check your traps to see if you snared anything tasty.
That script comes from here: http://bucardo.org/wiki/Tail_n_mail#Basic_Usage and requires you do:

sudo yum perl-Net-SMTP-SSL perl-Authen-SASL 

or the equivalent for your chosen operating system.


MASSIVE PROPS TO GRAHAM DUMPLETON FOR HIS ASSISTANCE WITH THIS. Give the bloke a donation if you can, he most definitely deserves it: http://code.google.com/p/modwsgi/wiki/HowToContributeBack
