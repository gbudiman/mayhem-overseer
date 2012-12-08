# -*- coding: utf-8 -*-
from Announcer import Announcer
import signal
import sys

if len(sys.argv) == 1:
	print 'Usage: python MayhemOverseer.py <your message here>'
else:
	interval = 330
	announcer = Announcer(interval)
	message = ' '.join(sys.argv[e] for e in xrange(1, len(sys.argv)));
	
	announcer.prepare(message).send();
	exit(0);