# -*- coding: utf-8 -*-
from xml.dom.minidom import parseString
from xml.dom.minidom import Node

f = open('scratchspace_canada.txt')
text = f.read()
dom = parseString(text)
xmlTag = dom.getElementsByTagName('option')
for tag in xmlTag:
	for data in tag.childNodes:
		if data.nodeType == Node.TEXT_NODE:
			print "".join(("\t", tag.getAttribute("value"), " => \"", data.data.encode('ascii', 'replace'), "\","))
