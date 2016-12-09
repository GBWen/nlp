# -*- coding: utf-8 -*-

import jieba.posseg as pseg

wordList = []
file = open(r'./true_short.txt.bak', 'r').read()
wfile = open('./true_short.txt','w')
words = list(pseg.cut(file))
for w in words :
	wordList.append(w.word)

# 去除停用词
stopwords = []
for line in open("stopword.txt"):
	line = line.strip('\n')
	line = line.strip(' ')
	stopwords.append(line)
print stopwords
for w in wordList :
	if w in stopwords :
		wordList.remove(w)
for w in wordList :
	wfile.write(w.encode('utf-8'))
