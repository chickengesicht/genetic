#vortragsperfekt: mehrdimensionale liste mit zeitfensterdaten
#schuelerperfekt: mehrdimensionale liste mit gewählten vortragen
#genarray: jeder schüler als einzelner array, pro schüler zwei arrays mit je einem vortrag und einem Zeitfenster
import random,time
schuelerperfekt=[]
vortragsperfekt=[]
millis = int(round(time.time() * 1000))
minSinZFproV=5
maxSinZFproV=25
vortragsanz=67
schueleranz=320
genanz=100
mutrate=0.003
for a in range(schueleranz):  #zufällige wahlen zu testzwecken
	schuelerperfekt.append([random.randint(1,vortragsanz),random.randint(1,vortragsanz),random.randint(1,vortragsanz)])
for a in range(vortragsanz):
	rin=[random.randint(1,3)]
	for c in range(2):
		b=random.randint(1,3)
		if not(b in rin):
			rin.append(b)
	vortragsperfekt.append(rin)
def randomgens(anz):
	result=[]
	for a in range(anz):
		result.append([]);
		for b in range(schueleranz):
			result[a].append([[random.randint(1,3),random.randint(1,vortragsanz)],[random.randint(1,3),random.randint(1,vortragsanz)]]);
	return result
def fitness(gene):
	fitlist=[]
	gencount=0;
	for s in gene:
		fitlist.append(0);
		vschuel=[]
		for a in range(vortragsanz):
			vschuel.append([0,0,0])
		scount=0
		for vz in s:
			for z in vz:
				vschuel[z[1]-1][z[0]-1]+=1
				if z[1]!=schuelerperfekt[scount][0] and z[1]!=schuelerperfekt[scount][1]:
					if z[1]!=schuelerperfekt[scount][2]:
						fitlist[gencount]+=5
					else:
						fitlist[gencount]+=1
			if vz[0][1]==vz[1][1]:
				fitlist[gencount]+=1000
			scount+=1	
		vcount=0
		for a in vschuel:
			zfcount=0
			for b in a:
				zfcount+=1
				if b>maxSinZFproV:
					fitlist[gencount]+=1000
				elif b<minSinZFproV and b!=0:
					fitlist[gencount]+=1000
				elif b!=0 and not (zfcount in vortragsperfekt[vcount]):
					fitlist[gencount]+=1000
			vcount+=1
		gencount+=1	
	return fitlist
def createnewgens(gene,fitlist):
	newgene=[]
	for a in gene:
		pass
gene=randomgens(genanz)
fitnesses=fitness(gene)
for a in fitnesses:
	print (a)
print (int(round(time.time() * 1000))-millis)