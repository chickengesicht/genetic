#Import Wahldaten from csv. Ziel: schuelerperfekt=[[w1, w2, w3], [w1, w2, w3] ...]
import csv
def getsperfekt():
	schuelerperfekt=[]
	with open('Wahlen.csv', newline = '') as csvfile:
		while 1:
			line = csvfile.readline()
			if line == "END": 
				break
			list = line.split(';')
			del list[3]
			for i in range(0,len(list)):
				list[i]=int(list[i])
			schuelerperfekt.append(list)
	print (schuelerperfekt)
	return schuelerperfekt