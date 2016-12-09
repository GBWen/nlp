# -*- coding: utf-8 -*-

from gensim.models import word2vec
import logging
import jieba.posseg as pseg
import numpy as np
import math

# 训练模型
logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level = logging.INFO)
sentences = word2vec.Text8Corpus("./description.txt")
model = word2vec.Word2Vec(sentences, trim_rule = None, min_count = 3, window = 8, size = 200)

# 保存模型
model.save("description.model")

# 加载模型
model = word2vec.Word2Vec.load("description.model")

# # 计算两个词的相似度/相关程度
# y1 = model.similarity("paperless", "Magic")
# print y1
# print "--------\n"

# 计算某个词的相关词列表
y2 = model.most_similar("data", topn=20)  # 20个最相关的
for item in y2:
	print item[0], item[1]
print "--------\n"

#构造词库
wordList = []
file = open(r'./description.txt', 'r').read()
words = list(pseg.cut(file))
# writefile = open('./words.txt','w')
for w in words :
	if w.flag != 'x'  and  w.flag != 'm' :  
		wordList.append(w.word)
		# print w.flag + " " +w.word
		# writefile.write(w.word)
		# writefile.write("\n")
# print len(wordList)
wordSet = set(wordList)
#print len(wordSet)
#print wordSet
wordList2 = []
for w in wordSet :
	try:
		y1 = model.similarity(w, "AI")
		if y1>0 :
			wordList2.append(w)
	except:
		pass
N = len(wordList2)

# 去除停用词
stopwords = []
for line in open("stopword.txt"):
	line = line.strip('\n')
	line = line.strip(' ')
	stopwords.append(line)
# print stopwords
for w in wordList2 :
	if w in stopwords :
		wordList2.remove(w)
N = len(wordList2)
# print wordList2

# 每条description 转化成向量
Num = 5
isAI=[] 
for i in range(Num): 
	isAI.append([]) 
	for j in range(N): 
		isAI[i].append(0) 
isnotAI=[] 
for i in range(Num): 
	isnotAI.append([]) 
	for j in range(N): 
		isnotAI[i].append(0) 
for i in range(1,Num+1) :
	trueFile = open(r'./true/%d.txt' % i, 'r').read()
	# print trueFile
	trueWords = []
	trueWords = list(pseg.cut(trueFile))
	trueWordList = []
	for w in trueWords :
		if w.flag != 'x'  and  w.flag != 'm' :  
			trueWordList.append(w.word)
	for w in trueWordList :
		if w in stopwords :
			trueWordList .remove(w)
	M = len(trueWordList)
	print i
	print M
	print trueWordList
	for j in range(0,N) :
		Max = 0
		# Ave = 0
		# count = 0
		for k in range(0,M) : 
			try:		
				y = model.similarity(wordList2[j], trueWordList[k])
				if y > Max :
					Max = y
				# Ave = y + Ave
				# count = count +1
			except:
				pass
		isAI[i-1][j] = Max
		# isAI[i-1][j] = Ave / count
for i in range(1,Num+1) :
	falseFile = open(r'./false/%d.txt' % i, 'r').read()
	falseWords = list(pseg.cut(falseFile))
	falseWordList = []
	for w in falseWords :
		if w.flag != 'x'  and  w.flag != 'm' :  
			falseWordList.append(w.word)
	for w in falseWordList :
		if w in stopwords :
			falseWordList .remove(w)
	M = len(falseWordList)
	print i
	print M
	print falseWordList
	for j in range(0,N) :
		Max = 0
		for k in range(0,M) : 
			try:		
				y = model.similarity(wordList2[j], falseWordList[k])
				if y > Max :
					Max = y
			except:
				pass
		isnotAI[i-1][j] = Max


for i in range(0,N) :
	print isAI[0][i], isAI[1][i], isAI[2][i], isAI[3][i]

for i in range(0,N) :
	print isnotAI[0][i], isnotAI[1][i], isnotAI[2][i], isnotAI[3][i]

# 余弦相似度
for i in range(0,3) :
	x = np.array(isAI[i])
	y = np.array(isnotAI[i])
	Lx = np.sqrt(x.dot(x))
	Ly = np.sqrt(y.dot(y))
	print Lx
	print Ly
	cosAngle = x.dot(y)/(Lx*Ly)
	print cosAngle
print "\n"

for i in range(0,3) :
	x = np.array(isAI[i])
	y = np.array(isAI[i+1])
	Lx = np.sqrt(x.dot(x))
	Ly = np.sqrt(y.dot(y))
	print Lx
	print Ly
	cosAngle = x.dot(y)/(Lx*Ly)
	print cosAngle
print "\n"

for i in range(0,3) :
	x = np.array(isnotAI[i])
	y = np.array(isnotAI[i+1])
	Lx = np.sqrt(x.dot(x))
	Ly = np.sqrt(y.dot(y))
	print Lx
	print Ly
	cosAngle = x.dot(y)/(Lx*Ly)
	print cosAngle
print "\n"













