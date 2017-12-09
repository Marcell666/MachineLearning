from string import punctuation
# os e para iterar em arquivos
import os

positiveSet = set()
negativeSet = set()
PosPoints = dict()
NegPoints = dict()

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
            print('checando', word)
            # se a palavra ja foi encontrada antes em outro arquivo que tambem e positivo
            if word in positiveSet and len(word) > 3:
                print('achei de novo', word)
                # vamos aumentar o peso da palavra
                PosPoints[word] = PosPoints[word] + 1
            # PosPoints.setdefault(word,[1,'true']) nao sei o que e isso
            # se a palavra nao foi encontrada
            elif len(word) > 3:
                print('adicionando', word)
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
            print('checando', word)
            # se a palavra ja foi encontrada antes em outro arquivo que tambem e negativo
            if word in negativeSet and len(word) > 3:
                print ('achei de novo', word)
                # vamos aumentar o peso da palavra
                NegPoints[word] = NegPoints[word] + 1
            # NegPoints.setdefault(word,[1,'true']) nao sei o que e isso
            # se a palavra nao foi encontrada
            elif len(word) > 3:
                print ('adicionando', word)
                # coloco ela na lista de palavras
                negativeSet.add(word)
                # e coloco com o valor 0 no set e o tempo atual
                NegPoints.setdefault(word, 1)

def cleanSets(NegWeightCut, PosWeightCut):

    for word in positiveSet.copy():
        if word in negativeSet.copy():
            temp = PosPoints[word]
            PosPoints[word] -= NegPoints[word]
            NegPoints[word] -= temp

    for word in negativeSet.copy():
        if NegPoints[word] < NegWeightCut:
            negativeSet.remove(word)
            NegPoints.pop(word)

    for word in positiveSet.copy():
        if PosPoints[word] < PosWeightCut:
            positiveSet.remove(word)
            PosPoints.pop(word)

def validateNewReview(sentence):

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
        # trainingDataSet('positive',sentence)
    elif points < 0:
        print('That was a negative review! ')
        # trainingDataSet('negative', sentence)
    else:
        print('That was an unconclusive review... ')
    print(points)
    return points

def main():

    # text = open('0_2.txt', 'r')
    # trainingDataSet('negative', text.read())
    # text = open('meuExemplo.txt', 'r')
    # trainingDataSet('negative', text.read())
    posTrainings = 0
    negTrainings = 0
    # caminho para pasta com os negativos
    pathNeg = 'ex/'
    # caminho para pasta com os positivos
    pathPos = 'exPos/'

    # aqui passamos por todos os arquivos e colocamos eles no hash/set
    for filename in os.listdir(pathNeg):
        filename = pathNeg + filename
        f = open(filename, 'r')
        trainingDataSet('negative', f.read())
        negTrainings += 1
        f.close()

    # fazemos o mesmo com os arquivos positivos
    for filename in os.listdir(pathPos):
        filename = pathPos + filename
        f = open(filename, 'r')
        trainingDataSet('positive', f.read())
        posTrainings += 1
        f.close()

    cleanSets((negTrainings/10), (posTrainings/10))

    # entao colocamos num arquivo so, com os pesos
    finalFile = open('outputN.txt', 'w+')
    for key, value in NegPoints.items():
        print(key, value)
        finalFile.write(str(key) + ' ' + str(value) + '\n')
    finalFile.close()

    finalFile = open('outputP.txt','w+')
    for key, value in PosPoints.items():
        print(key, value)
        finalFile.write(str(key) + ' ' + str(value) + '\n')
    finalFile.close()

    # validFile = open('ValidNeg/12492_4.txt')
    # validateNewReview(validFile.read())

    validFile = open('ValidPos/999_8.txt')
    validateNewReview(validFile.read())

    print('Positive Trainings: ' + str(posTrainings))
    print('Negative Trainings: ' + str(negTrainings))
    # E ao inves de colocar um limite. Podemos simplesmente separar os arquivos de treinamento e de validacao em pastas diferentes.


main()
