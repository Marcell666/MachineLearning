from string import punctuation
import time
# os e para iterar em arquivos
import os

positiveSet = set()
negativeSet = set()
PosPoints = dict()
NegPoints = dict()
totalPosReviews = 0
totalNegReviews = 0
TotalTrainings = 0

def uniqueWords(sentence):
    return set(sentence.translate(str.maketrans(' ',' ', punctuation)).lower().split())

def trainingDataSet(classification, sentence):
    global positiveSet
    global negativeSet
    global PosPoints
    global NegPoints

    if classification == 'positive':
        # retirando palavras repetidas, e pontuacao
        wordSet = uniqueWords(sentence)
        for word in wordSet:
            # print('checando', word)
            # se a palavra ja foi encontrada antes em outro arquivo que tambem e positivo
            if word in positiveSet and len(word) > 3:
                # print('achei de novo', word)
                # vamos aumentar o peso da palavra
                PosPoints[word] = PosPoints[word] + 1
            # PosPoints.setdefault(word,[1,'true']) nao sei o que e isso
            # se a palavra nao foi encontrada
            elif len(word) > 3:
                # print('adicionando', word)
                # coloco ela na lista de palavras
                positiveSet.add(word)
                # e coloco com o valor 0 no set e o tempo atual
                PosPoints.setdefault(word, 1)

    #		for key, value in PosPoints.iteritems():
    #			print key, value
    elif classification == 'negative':
        # retirando palavras repetidas, e pontuacao
        wordSet = uniqueWords(sentence)
        for word in wordSet:
            # print('checando', word)
            # se a palavra ja foi encontrada antes em outro arquivo que tambem e negativo
            if word in negativeSet and len(word) > 3:
                # print('achei de novo', word)
                # vamos aumentar o peso da palavra
                NegPoints[word] = NegPoints[word] + 1
            # NegPoints.setdefault(word,[1,'true']) nao sei o que e isso
            # se a palavra nao foi encontrada
            elif len(word) > 3:
                # print('adicionando', word)
                # coloco ela na lista de palavras
                negativeSet.add(word)
                # e coloco com o valor 0 no set e o tempo atual
                NegPoints.setdefault(word, 1)

def cleanSets(NegWeightCut, PosWeightCut):

    for word in negativeSet.copy():
        if NegPoints[word] < NegWeightCut:
            negativeSet.remove(word)
            NegPoints.pop(word)

    for word in positiveSet.copy():
        if PosPoints[word] < PosWeightCut:
            positiveSet.remove(word)
            PosPoints.pop(word)

def validateNewReview(sentence):
    global totalNegReviews
    global totalPosReviews
    global TotalTrainings

    wordSet = uniqueWords(sentence)
    points = 0
    for word in wordSet:
        if word in positiveSet:
            points += PosPoints[word]

    for word in wordSet:
        if word in negativeSet:
            points -= NegPoints[word]

    if points > 0:
        print('That was a positive review! ')
        trainingDataSet('positive',sentence)
        TotalTrainings += 1
        totalPosReviews += 1
    elif points < 0:
        print('That was a negative review! ')
        trainingDataSet('negative', sentence)
        TotalTrainings += 1
        totalNegReviews += 1
    else:
        print('That was an inconclusive review... ')
    print(points)
    return points

def main():
    global TotalTrainings
    posTrainings = 0
    negTrainings = 0

    # caminho para pasta com os negativos
    pathNeg = 'TrainingNeg/'
    # caminho para pasta com os positivos
    pathPos = 'TrainingPos/'

    maxTrainings = int(input('Type the number of trainings: '))
    print('Started Training. Please wait...')
    start_time = time.time()
    # aqui passamos por todos os arquivos e colocamos eles no hash/set
    for filename in os.listdir(pathNeg):
        if negTrainings >= maxTrainings:
            break
        filename = pathNeg + filename
        f = open(filename, 'r', encoding="Latin-1")
        trainingDataSet('negative', f.read())
        negTrainings += 1
        f.close()

    # fazemos o mesmo com os arquivos positivos
    for filename in os.listdir(pathPos):
        if posTrainings >= maxTrainings:
            break
        filename = pathPos + filename
        f = open(filename, 'r', encoding="Latin-1")
        trainingDataSet('positive', f.read())
        posTrainings += 1
        f.close()

    TotalTrainings = posTrainings
    # limpo os sets com palavras que possam ser irrelevantes ou pouco apareceram
    cleanSets((TotalTrainings/6), (TotalTrainings/7))

    # começo a contar o tempo de treinamento
    training_time = (time.time() - start_time)
    # default paths
    validPathPos = 'validPos/'
    validPathNeg = 'validNeg/'
    totalValid = 0
    print('Finished Training...')
    maxClass = int(input('Type the number of reviews to classify: '))
    path = input('Enter the path of the reviews: ')

    if path.lower() == 'defaultp':
        path = validPathPos
    elif path.lower() == 'defaultn':
        path = validPathNeg

    # classifico enquanto houver arquivo ou eu não ultrapassar o limite de classificações
    classifying_time = time.time()
    for filename in os.listdir(path):
        if totalValid >= maxClass:
            break
        if (TotalTrainings % 250) == 0:
            cleanSets((TotalTrainings / 6), (TotalTrainings / 7))
        filename = path + filename
        validFile = open(filename, encoding='utf-8')
        print('Reading file: ',filename)
        validateNewReview(validFile.read())
        totalValid += 1

    classifying_finalTime = time.time() - classifying_time

    # pego o tipo das reviews a serem classificadas, só para mostrar a precisão
    typeofReviews = input('What was the classification of the reviews? ')

    if typeofReviews.lower() == 'negative':
        percent = 100.0 - (totalPosReviews/(totalPosReviews+totalNegReviews)) * 100
    elif typeofReviews.lower() == 'positive':
        percent = 100.0 - (totalNegReviews / (totalPosReviews + totalNegReviews)) * 100

    # mostro os resultados obtidos
    print('Positive Reviews: ', totalPosReviews)
    print('Negative Reviews: ', totalNegReviews)

    # mostro o percentual de precisão
    print('Correctness: ', percent, '%')
    print('Elapsed Time while training: ', training_time)
    print('Elapsed Time while classifying: ', classifying_finalTime)

    input()


main()
