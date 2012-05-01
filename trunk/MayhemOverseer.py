# -*- coding: utf-8 -*-
from MayhemMiner import MayhemMiner
import sys

if len(sys.argv) == 1:
	miner = MayhemMiner(1)
else:
	oList = list()
	for d in range(1, len(sys.argv)):
		if sys.argv[d] == '-h':
			print 'Usage: python MayhemOverseer.py -{x}:{argument} -{x}:{argument} ...'
			print 'Where -{x}:{argument} is as follows:'
			print '-h \t\t You\'re getting it now'
			print '-o:recollect \t Continue from pickled dictionary'
			print '-o:testonly \t Run crawler without updating database'
			sys.exit(0)
		if sys.argv[d] == '-o:recollect':
			oList.append('recollect')
		if sys.argv[d] == '-o:testonly':
			oList.append('testonly')
	
	if 'recollect' in oList and 'testonly' in oList:
		print '-o:recollect and -o:testonly cannot be active at the same time'
	else:
		miner = MayhemMiner(1, oList)