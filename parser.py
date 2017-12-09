from string import maketrans
from string import punctuation
#nao sei se esse e redundante com os de cima
import string 
#os e para iterar em arquivos
import os


global positiveSet
#guarda as palavras encontradas em reviews positivas, sem repeti-las
global negativeSet
#guarda as palavras encontradas em reviews negativas, sem repeti-las
global PosPoints
#guarda a quantidade de vezes que uma determinada palavra foi encontrada em reviews positivos diferentes
global NegPoints
#guarda a quantidade de vezes que uma determinada palavra foi encontrada em reviews negativos diferentes
global maiorPeso
#usado para guardar a maior ocorrencia encontrada
#assim posso usa-la numa regra de 3


positiveSet = set()
negativeSet = set()
PosPoints = dict()
NegPoints = dict()


#vou usar part1 como treinamento e part2 como validacao
#caminho para pasta com os negativos
pathNeg = 'part1/neg/'
#caminho para pasta com os positivos
pathPos = 'part1/pos/'

maiorPeso = 0


def uniqueWords(sentence):
	return set(sentence.translate(string.maketrans('',''), punctuation).lower().split())

def trainingDataSet(classification, sentence):
	global positiveSet
	global negativeSet
	global PosPoints
	global NegPoints
	global maiorPeso

	if classification == 'positive':
		# retirando palavras repetidas, e pontuacao
		wordSet = uniqueWords(sentence)
		for word in wordSet:
			if len(word) >= 4:
				#print 'checando ', word
				#se a palavra ja foi encontrada antes em outro arquivo que tambem e positivo
				if word in positiveSet:
					#print 'achei de novo', word
					#vamos aumentar o peso da palavra
					PosPoints[word] =  PosPoints[word] + 1
				#se a palavra nao foi encontrada
				else:
					#print 'adicionando', word
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
			if len(word) >= 4:
				#print 'checando ', word
				#se a palavra ja foi encontrada antes em outro arquivo que tambem e negativo
				if word in negativeSet:
					#print 'achei de novo', word
					#vamos aumentar o peso da palavra
					NegPoints[word] =  NegPoints[word] + 1
				#se a palavra nao foi encontrada
				else:
					#print 'adicionando', word
					#coloco ela na lista de palavras
					negativeSet.add(word)
					#e coloco com o valor 0 no set e o tempo atual
					NegPoints.setdefault(word, 1)

#		for key, value in NegPoints.iteritems():
#			print key, value

#


def compara(a, b, taxa):
	print 'comparando ', a, ' com ', b, 'taxa', (float(b)/float(a))*100 , ' / ', taxa
	if taxa == 100:
		return False
	elif a == b :
		return True
	elif a>b:
		print float(b)/a 
		return (float(b)/float(a))*100 > taxa
	else:
		print a/float(b)
		return (a/float(b))*100 > taxa


#retira as palavras comuns que possuem uma taxa de semelhanca de pesos maior do que um valor fornecido
#essa funcao tem o intuito de retirar palavras neutras
#as palavras neutras provavelmente paracem nos dois textos em quantidades parecidas
#uma palavra como 'good' deve aparecer bem mais em reviews positivas do que negativas
#mas talvez apareca nas duas. Nao queremos retirar palavras so de elas aparecerem, uma tolerancia e necessaria.
#essa tolerancia e a taxa de semelhanca de pesos
#se os pesos sao muito semelhantes entao deve ser uma palavra comum e neutra, como uma preposicao.
def retiraIntersecao(taxa):
	global positiveSet
	global negativeSet
	global PosPoints
	global NegPoints
	global maiorPeso
	retirar = list()

	for word in positiveSet:
		print word		
		if word in negativeSet:
			if compara(PosPoints[word], NegPoints[word], taxa):
				print 'retirando', word
				retirar.insert(0, word)
	for word in retirar:
		positiveSet.remove(word)
		PosPoints.pop(word)
		negativeSet.remove(word)
		NegPoints.pop(word)

	for word in positiveSet:		
		#guardando a maior ocorrencia encontrada ate agora
		if maiorPeso < PosPoints[word]:
			maiorPeso = PosPoints[word]

	for word in negativeSet:		
		#guardando a maior ocorrencia encontrada ate agora
		if maiorPeso < NegPoints[word]:
			maiorPeso = NegPoints[word]




#aqui passamos por todos os arquivos e colocamos eles no hash/set
for filename in os.listdir(pathNeg):
	filename = pathNeg+filename
	f = open(filename, 'r')
	trainingDataSet('negative', f.read())

#fazemos o mesmo com os arquivos positivos
for filename in os.listdir(pathPos):
	filename = pathPos+filename
	f = open(filename, 'r')
	trainingDataSet('positive', f.read())

#essa taxa e uma porcentagem
taxa = 85
maiorPeso = 0

retiraIntersecao(taxa)


#entao colocamos num arquivo so, com os pesos
finalFile = open('outputN','w+')
finalFile.write(str(maiorPeso) + '\n')
for key, value in NegPoints.iteritems():
	#print key, value
	if value > 2:
		finalFile.write(str(key) + ' ' + str(value) + '\n')

finalFile = open('outputP','w+')
finalFile.write(str(maiorPeso) + '\n')
for key, value in PosPoints.iteritems():
	#print key, value
	if value > 2:
		finalFile.write(str(key) + ' ' + str(value) + '\n')

#Falta colocar a tal nota de corte
#E ao inves de colocar um limite. Podemos simplesmente separar os arquivos de treinamento e de validacao em pastas diferentes.
