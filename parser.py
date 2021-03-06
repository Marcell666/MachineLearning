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
global tamVetor
global totalSet
global totalHash


positiveSet = set()
negativeSet = set()
PosPoints = dict()
NegPoints = dict()
totalSet = set()
totalHash = dict()


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
	retirar = set()

	for word in positiveSet:
		if PosPoints[word] < 100:
			print 'pouco frequente, retirando ', word
			retirar.add(word)
		elif word in negativeSet:
			if compara(PosPoints[word], NegPoints[word], taxa):
				print 'parece neutra, retirando ', word
				retirar.add( word)
		else:
			print 'deixando ', word
	for word in negativeSet:
		if NegPoints[word] < 100:
			retirar.add(word)

	for word in retirar:
		if word in positiveSet:
			positiveSet.remove(word)
			PosPoints.pop(word)
		if word in negativeSet:
			negativeSet.remove(word)
			NegPoints.pop(word)

def uniao():
	global positiveSet
	global negativeSet
	global PosPoints
	global NegPoints
	global maiorPeso
	global totalHash
	global totalSet

	totalSet = set()
	totalHash = dict()
	i = 0

	for word in positiveSet:
		if word not in totalSet:
			totalSet.add(word)
			#colocando index
			totalHash.setdefault(word, i)
			i = i+1
		#guardando a maior ocorrencia encontrada ate agora
		if maiorPeso < PosPoints[word]:
			maiorPeso = PosPoints[word]

	for word in negativeSet:		
		if word not in totalSet:
			totalSet.add(word)
			#colocando index
			totalHash.setdefault(word, i)
			i = i+1
		#guardando a maior ocorrencia encontrada ate agora
		if maiorPeso < NegPoints[word]:
			maiorPeso = NegPoints[word]

def contaOcorrencia(sentenca, f):
	global positiveSet
	global negativeSet
	global PosPoints
	global NegPoints
	global maiorPeso
	global totalHash
	global totalSet

	# retirando palavras repetidas, e pontuacao
	wordSet = uniqueWords(sentenca)

	#posicoesCriticas = list()
	for word in wordSet:
		#if word not in totalHash:
			#print 'nao encontrado ', word
		if word in totalHash:
			f.write(str(totalHash[word]) + ' ' )
			#posicoesCriticas.insert(0, totalHash[word])
			#print totalHash[word]
	#posicoesCriticas.sort()


	#eu fiz de uma forma complicada aqui, mas a razao e que eu precisava garantir que os dados seriam gravados no arquivo precisamente na mesma ordem de palvras.
	# por isso associei um index a cada palavra e estou percorrendo o hash e verificando se as palavras existem ou nao neste exemplo.
	# se a palvra existir guardo nauqela posicao o numero 1, indicando ocorrencia
	#se nao, guardo naquela posicao o numero 0
	#e = 0
	#i = 0
	#tam = len(posicoesCriticas)
	#for word in totalSet:
	#	if e<tam and posicoesCriticas[e] == i:
	#		#f.write(str(1) + ' ')
	#		print str(1) + ' '
	#		e = e + 1
	#	else:
	#		print str(0) + ' '
	#		#f.write(str(0) + ' ')
	#	i = i + 1
	


	f.write('\n')


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
uniao()

#entao colocamos num arquivo so, com os pesos
finalFile = open('outputN','w+')
finalFile.write(str(maiorPeso) + '\n')
for key, value in NegPoints.iteritems():
	#print key, value
	finalFile.write(str(key) + ' ' + str(value) + '\n')

finalFile = open('outputP','w+')
finalFile.write(str(maiorPeso) + '\n')
for key, value in PosPoints.iteritems():
	#print key, value
	finalFile.write(str(key) + ' ' + str(value) + '\n')
#---------------------------------------------------------------------

#agora passamos por todos os arquivos novamente, dessa vez comparando eles com o set total e colocando em um outro arquivo


pathNegDest = 'dest/neg/dest'
pathPosDest = 'dest/pos/dest'

fDest = open(pathNegDest, 'w')
for filename in os.listdir(pathNeg):
	filename = pathNeg+filename
	f = open(filename, 'r')
	contaOcorrencia(f.read(), fDest)

fDest = open(pathPosDest, 'w')
for filename in os.listdir(pathPos):
	filename = pathPos+filename
	f = open(filename, 'r')
	contaOcorrencia(f.read(), fDest)
