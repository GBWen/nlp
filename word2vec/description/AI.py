from numpy import *
                
def createVocabList(dataSet):
    vocabSet = set([])  #create empty set
    for document in dataSet:
        vocabSet = vocabSet | set(document) #union of the two sets
    return list(vocabSet)

def setOfWords2Vec(vocabList, inputSet):
    returnVec = [0]*len(vocabList)
    for word in inputSet:
        if word in vocabList:
            returnVec[vocabList.index(word)] = 1
        else: print "the word: %s is not in my Vocabulary!" % word
    return returnVec

def trainNB0(trainMatrix,trainCategory):
    numTrainDocs = len(trainMatrix)
    numWords = len(trainMatrix[0])
    pAbusive = sum(trainCategory)/float(numTrainDocs)
    p0Num = ones(numWords); p1Num = ones(numWords)      #change to ones()
    p0Denom = 2.0; p1Denom = 2.0                        #change to 2.0
    for i in range(numTrainDocs):
        if trainCategory[i] == 1:
            p1Num += trainMatrix[i]
            p1Denom += sum(trainMatrix[i])
            # print i,trainMatrix[i]
        else:
            p0Num += trainMatrix[i]
            p0Denom += sum(trainMatrix[i])
    # print p1Num
    p1Vect = log(p1Num/p1Denom)          #change to log()
    p0Vect = log(p0Num/p0Denom)          #change to log()
    return p0Vect,p1Vect,pAbusive

def classifyNB(vec2Classify, p0Vec, p1Vec, pClass1):
    p1 = sum(vec2Classify * p1Vec) + log(pClass1)    #element-wise mult
    p0 = sum(vec2Classify * p0Vec) + log(1.0 - pClass1)
    if p1 > p0:
        return 1
    else:
        return 0

def testingNB():
    listOPosts,listClasses = loadDataSet()
    myVocabList = createVocabList(listOPosts)
    trainMat=[]
    for postinDoc in listOPosts:
        trainMat.append(setOfWords2Vec(myVocabList, postinDoc))
    p0V,p1V,pAb = trainNB0(array(trainMat),array(listClasses))
    testEntry = ['love', 'my', 'dalmation']
    thisDoc = array(setOfWords2Vec(myVocabList, testEntry))
    print testEntry,'classified as: ',classifyNB(thisDoc,p0V,p1V,pAb)
    testEntry = ['stupid', 'garbage']
    thisDoc = array(setOfWords2Vec(myVocabList, testEntry))
    print testEntry,'classified as: ',classifyNB(thisDoc,p0V,p1V,pAb)

def bagOfWords2VecMN(vocabList, inputSet):
    returnVec = [0]*len(vocabList)
    for word in inputSet:
        if word in vocabList:
            returnVec[vocabList.index(word)] += 1
    return returnVec

# listOPosts,listClasses = loadDataSet()
# myVocabList = createVocabList(listOPosts)
# # print myVocabList
# trainMat = []
# for postinDoc in listOPosts:
#     trainMat.append(setOfWords2Vec(myVocabList,postinDoc))
# # print trainMat
# # p0V,p1V,pAb = trainNB0(trainMat,listClasses)
# # print p0V
# # print p1V
# # testingNB()

def textParse(bigString):    #input is big string, #output is word list
    import re
    listOfTokens = re.split(r'\W*', bigString)
    return [tok.lower() for tok in listOfTokens if len(tok) > 2]

def spamTest():
    sum = 0
    for p in range (1,101):
        docList=[]; classList = []; fullText =[]
        for i in range(1,101):
            wordList = textParse(open('./true/%d.txt' % i).read())
            docList.append(wordList)
            fullText.extend(wordList)
            classList.append(1)
            wordList = textParse(open('./false/%d.txt' % i).read())
            docList.append(wordList)
            fullText.extend(wordList)
            classList.append(0)
        vocabList = createVocabList(docList)#create vocabulary
        trainingSet = range(200); testSet=[]           #create test set
        for i in range(10):
            randIndex = int(random.uniform(0,len(trainingSet)))
            testSet.append(trainingSet[randIndex])
            del(trainingSet[randIndex]) 
        trainMat=[]; trainClasses = []
        for docIndex in trainingSet:#train the classifier (get probs) trainNB0
            trainMat.append(bagOfWords2VecMN(vocabList, docList[docIndex]))
            trainClasses.append(classList[docIndex])
        p0V,p1V,pSpam = trainNB0(array(trainMat),array(trainClasses))
        errorCount = 0
        for docIndex in testSet:        #classify the remaining items
            wordVector = bagOfWords2VecMN(vocabList, docList[docIndex])
            if classifyNB(array(wordVector),p0V,p1V,pSpam) != classList[docIndex]:
                errorCount += 1
                # print "classification error",docList[docIndex]
        print 'the error rate is: ',float(errorCount)/len(testSet)
        sum += float(errorCount)/len(testSet)
        #return vocabList,fullText
    print 'the average error rate is: ' ,sum / 100

spamTest()