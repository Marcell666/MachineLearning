from string import maketrans
from string import punctuation
import string 

global positiveSet
global PosPoints
global NegPoints
global negativeSet


positiveSet = set()
negativeSet = set()
PosPoints = dict()
NegPoints = dict()

def uniqueWords(sentence):
	return set(sentence.translate(string.maketrans('',''), punctuation).lower().split())

def trainingDataSet(classification, sentence):
	global positiveSet
	global negativeSet
	global PosPoints
	global NegPoints

	# retirando palavras repetidas, e pontuacao
	wordSet = uniqueWords(sentence)
	for word in wordSet:
#se ela ja foi encontrada antes
#e o tempo em que isso aconteceu e diferente do atual
# eu faco isso porque nao quero contar duas vezes uma palavra no mesmo arquivo.
# o tempo aumenta uma unidade a cada vez que mudo de arquivo
#
#eu espero que exista curto-circuito aqui
		print 'checando ', word
		#se a palavra ja foi encontrada antes em outro arquivo que tambem e positivo
		if word in positiveSet:
			print 'achei de novo', word
			#vamos aumentar o peso da palavra
			PosPoints[word] =  PosPoints[word] + 1
			#PosPoints.setdefault(word,[1,'true']) nao sei o que e isso
		#se a palavra nao foi encontrada
		else:
			print 'adicionando', word
			#coloco ela na lista de palavras
			positiveSet.add(word)
			#e coloco com o valor 0 no set e o tempo atual
			PosPoints.setdefault(word, 1)

	for key, value in PosPoints.iteritems():
		print key, value

text = open('0_2.txt','r')
trainingDataSet('negative', text.read())
text = open('meuExemplo.txt','r')
trainingDataSet('negative', text.read())
#trainingDataSet('negative','his costners around else')
#for word in negativeSet:
#	finalFile.write(word + '\n')
#for key in NegPoints:
#	print(key,NegPoints[key])

#print(input())

