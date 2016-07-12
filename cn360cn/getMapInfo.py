#!/usr/bin/python
# -*- coding: utf-8 -*-
import sys
reload(sys)
sys.setdefaultencoding('utf-8')

import urllib 
import json

'''
class getMapInfo:
    def __init__(self, file, addressTag, key = 'auwrk7q6rBxwTYQNOvpu42Q7XvaLu3eb'):
        self.file = file
        self.addressTag = addressTag
        self.key = key
        
    def process(self, query = None, radius = 1000):
        nameList = self.file.split('.')
        nameList.insert(-1, "_withMapInfo.")
        outFile = ""
        for str in nameList:
            outFile += str
        try:    
            with open(self.file, "r") as fin:
                try:
                    with open(outFile, "w+") as fout:
                        key = self.key
                        i = 0
                        for line in fin:
                            i += 1
                            try:
                                inData = json.loads(line)
                            except Exception, e:
                                print "There is a bad line at " + str(i)
                                continue
                            if inData.has_key(self.addressTag):
                                address = inData[self.addressTag].encode("utf-8")
                                url = "http://api.map.baidu.com/geocoder/v2/?address=" + address + "&output=json&ak=" + key
                                response = urllib.urlopen(url)
                                jsonData =json.loads(response.read())
                                if "result" in jsonData:
                                    if "location" in jsonData["result"]:
                                        if "lng" in jsonData ["result"]["location"]:
                                            inData['longitude'] = jsonData["result"]["location"]["lng"]
                                        if "lat" in jsonData["result"]["location"]:
                                            inData['latitude'] = jsonData["result"]["location"]["lat"]
                                    if "precise" in jsonData["result"]:
                                        inData['precise'] = jsonData["result"]["precise"]
                                    if "confidence" in jsonData["result"]:
                                        inData['confidence'] = jsonData["result"]["confidence"]
                                if not inData.has_key("longitude"):
                                    inData['longitude'] = 999.0
                                if not inData.has_key("latitude"):
                                    inData['latitude'] = 999.0
                                outLine = json.dumps(inData) + "\n"
                                fout.write(outLine.decode("unicode_escape"))
                except IOError as err1:
                    print('File in error: ' + err1)
        
        except IOError as err2:
            print('File out error: ' + err2)


file = "items_cn360cn3-1_3.jl"
tag = "address"
map = getMapInfo(file, tag)
map.process()
'''


class getMapInfo:
    def __init__(self, file):
        self.file = file
        self.dic = {u'56': u'\u7cbe\u7ec6\u5316\u5b66\u54c1', u'2904': u'\u91d1\u878d\u670d\u52a1', u'2828': u'\u521b\u610f\u8bbe\u8ba1', u'52': u'\u7eb8\u4e1a', u'2807': u'\u7269\u6d41\u670d\u52a1', u'2805': u'\u52a0\u5de5\u5e02\u573a', u'24': u'\u5e7f\u544a', u'26': u'\u54a8\u8be2', u'21': u'\u529e\u516c\u3001\u6587\u6559', u'23': u'\u5305\u88c5', u'28': u'\u5546\u52a1\u670d\u52a1', u'1': u'\u519c\u4e1a', u'3': u'\u670d\u88c5', u'2': u'\u98df\u54c1\u3001\u996e\u6599', u'5': u'\u7535\u5de5\u7535\u6c14', u'4': u'\u7eba\u7ec7\u3001\u76ae\u9769', u'7': u'\u6570\u7801\u3001\u7535\u8111', u'509': u'\u901a\u4fe1\u4ea7\u54c1', u'9': u'\u51b6\u91d1\u77ff\u4ea7', u'8': u'\u5316\u5de5', u'2604': u'\u516c\u53f8\u6ce8\u518c', u'1813': u'\u73a9\u5177', u'6': u'\u5bb6\u7528\u7535\u5668', u'2701': u'\u8fdb\u51fa\u53e3\u4ee3\u7406', u'15': u'\u5bb6\u5c45\u7528\u54c1', u'10208': u'\u4eea\u5668\u4eea\u8868', u'58': u'\u7167\u660e\u5de5\u4e1a', u'11': u'\u73af\u4fdd', u'10': u'\u80fd\u6e90', u'13': u'\u5efa\u7b51\u3001\u5efa\u6750', u'12': u'\u4ea4\u901a\u8fd0\u8f93', u'59': u'\u4e94\u91d1', u'14': u'\u673a\u68b0', u'17': u'\u793c\u54c1', u'16': u'\u533b\u836f\u3001\u4fdd\u517b', u'33': u'\u6c7d\u8f66', u'54': u'\u670d\u9970', u'57': u'\u7535\u5b50', u'30': u'\u5b89\u9632', u'53': u'\u4f20\u5a92\u3001\u5e7f\u7535', u'34': u'\u5370\u5237', u'55': u'\u6a61\u5851', u'18': u'\u8fd0\u52a8\u3001\u4f11\u95f2'}
    def process(self):
        nameList = self.file.split('.')
        nameList.insert(-1, "_category")
        outFile = ""
        for str in nameList:
            outFile += str
        try:
            with open(self.file, "r") as fin:
                try:
                    with open(outFile, "w+") as fout:
                        i = 0
                        for line in fin:
                            i += 1
                            try:
                                inData = json.loads(line)
                            except Exception, e:
                                print "There is a bad line at " + str(i)
                                continue

                            url = inData[url]
                            urlChip = url.split('/')
                            category = urlChip[-2]
                            if category in self.dic:
                                indata['category'] = category
                                outLine = json.dumps(inData) + "\n"
                                fout.write(outLine.decode("unicode_escape"))
                except IOError as err1:
                    print('File in error: ' + err1)

        except IOError as err2:
            print('File out error: ' + err2)

file = "items_cn360cn2016_1.jl"
map = getMapInfo(file)
map.process()
        
