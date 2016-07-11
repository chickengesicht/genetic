#Import Wahldaten from csv. Ziel: schuelerperfekt=[[w1, w2, w3], [w1, w2, w3] ...]

schuelerperfekt=[]

import csv
with open('Vortrag-Zeitfenster.csv', newline = '') as csvfile:
	while 1:
		line = csvfile.readline()
		if line == "END": 
			break
		list = line.split(';')
		for a in range(3,0,-1):
			try:
				b=int(list[a])
			except:
				del list[a]
		for i in range(0,len(list)):
			list[i]=int(list[i])
		schuelerperfekt.append(list)

print(schuelerperfekt)			
