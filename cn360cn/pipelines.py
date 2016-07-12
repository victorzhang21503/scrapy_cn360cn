#!/usr/bin/python
# -*- coding: utf-8 -*-
import sys
reload(sys)
sys.setdefaultencoding('utf-8')

import json
import codecs

class Cn360cnPipeline(object):
	def __init__(self):
		self.file = codecs.open('cn360cn_data.json', mode='wb', encoding='utf-8')

	def process_item(self, item, spider):
		line = json.dumps(dict(item)) + '\n'
		self.file.write(line.decode("unicode_escape"))
		return item

