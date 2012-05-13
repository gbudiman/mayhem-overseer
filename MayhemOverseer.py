# -*- coding: utf-8 -*-
from MayhemMiner import MayhemMiner
import sys

if len(sys.argv) == 1:
	miner = MayhemMiner(1, list())
else:
	oList = list()
	for d in range(1, len(sys.argv)):
		if sys.argv[d] == '-h':
			print 'Usage: python MayhemOverseer.py -{x}:{argument} -{x}:{argument} ...'
			print 'Where -{x}:{argument} is as follows:'
			print '-h \t\t You\'re getting it now'
			print '-o:recollect \t Continue from pickled dictionary'
			print '-o:testonly \t Run crawler without updating database'
			print
			print '-t:skipcasting \t Only index Members data'
			print '-t:skipmembers \t Only index Casting data'
			sys.exit(0)
		if sys.argv[d] == '-o:recollect':
			oList.append('recollect')
		if sys.argv[d] == '-o:testonly':
			oList.append('testonly')
		if sys.argv[d] == '-t:skipcasting':
			oList.append('skipcasting')
		if sys.argv[d] == '-t:skipmembers':
			oList.append('members')
	
	if 'recollect' in oList and 'testonly' in oList:
		print '-o:recollect and -o:testonly cannot be active at the same time'
	else:
		miner = MayhemMiner(1, oList)