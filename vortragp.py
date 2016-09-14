#Import Wahldaten from csv. Ziel: schuelerperfekt=[[w1, w2, w3], [w1, w2, w3] ...]
import csv
def getvperfekt():
	vortragperfekt=[]
	with open('Vortrags.csv', newline = '') as csvfile:
		while 1:
			line = csvfile.readline()
			if line == "END": 
				break
			list = line.split(';')
			del list[3]
			raus=[]
			for i in range(0,len(list)):
				if list[i]!="NULL":
					raus.append(int(list[i])-1)
			vortragperfekt.append(raus)
	return vortragperfekt