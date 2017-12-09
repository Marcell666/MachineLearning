from string import maketrans
from string import punctuation
import string 
#os e para iterar em arquivos
import os

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

	if classification == 'positive':
		# retirando palavras repetidas, e pontuacao
		wordSet = uniqueWords(sentence)
		for word in wordSet:
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

#		for key, value in PosPoints.iteritems():
#			print key, value
	elif classification == 'negative':
		# retirando palavras repetidas, e pontuacao
		wordSet = uniqueWords(sentence)
		for word in wordSet:
			print 'checando ', word
			#se a palavra ja foi encontrada antes em outro arquivo que tambem e negativo
			if word in negativeSet:
				print 'achei de novo', word
				#vamos aumentar o peso da palavra
				NegPoints[word] =  NegPoints[word] + 1
				#NegPoints.setdefault(word,[1,'true']) nao sei o que e isso
			#se a palavra nao foi encontrada
			else:
				print 'adicionando', word
				#coloco ela na lista de palavras
				negativeSet.add(word)
				#e coloco com o valor 0 no set e o tempo atual
				NegPoints.setdefault(word, 1)

#		for key, value in NegPoints.iteritems():
#			print key, value

text = open('0_2.txt','r')
trainingDataSet('negative', text.read())
text = open('meuExemplo.txt','r')
trainingDataSet('negative', text.read())


#caminho para pasta com os negativos
pathNeg = 'ex/'
#caminho para pasta com os positivos
#pathPos = 'exPos'

#aqui passamos por todos os arquivos e colocamos eles no hash/set
for filename in os.listdir(pathNeg):
	filename = pathNeg+filename
	f = open(filename, 'r')
	trainingDataSet('negative', f.read())

#entao colocamos num arquivo so, com os pesos
finalFile = open('outputN','w+')
for key, value in NegPoints.iteritems():
	print key, value
	finalFile.write(str(key) + ' ' + str(value) + '\n')

#fazemos o mesmo com os arquivos positivos
#for filename in os.listdir(pathPos):
#	filename = pathPos+filename
#	f = open(filename, 'r')
#	trainingDataSet('positive', f.read())

#finalFile = open('outputP','w+')
#for key, value in PosPoints.iteritems():
#	print key, value
#	finalFile.write(str(key) + ' ' + str(value) + '\n')

#Falta colocar a tal nota de corte
#E ao inves de colocar um limite. Podemos simplesmente separar os arquivos de treinamento e de validacao em pastas diferentes.

