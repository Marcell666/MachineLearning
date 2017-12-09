import os

path = 'ex/'

for filename in os.listdir(path):
	filename = path+filename
	f = open(filename, 'r')
	content = f.read()
	print filename, len(content)



