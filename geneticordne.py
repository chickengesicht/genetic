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
genanz=1000
maxmutrate=0.01
dieweights=[]
for a in range(genanz):
	dieweights.append(60.0/(a+3))   #probability function
for a in range(schueleranz):  #zufällige wahlen zu testzwecken
	schuelerperfekt.append([random.randint(1,vortragsanz),random.randint(1,vortragsanz),random.randint(1,vortragsanz)])
for a in range(vortragsanz):
	rin=[random.randint(1,3)]
	for c in range(2):
		b=random.randint(1,3)
		if not(b in rin):
			rin.append(b)
	vortragsperfekt.append(rin)
def weighted_choice(weights):  #aus dem internet
    rnd = random.random() * sum(weights)
    for i, w in enumerate(weights):
        rnd -= w
        if rnd < 0:
            return i
def randomgens(anz):
	result=[]
	for a in range(anz):
		result.append([])
		for b in range(schueleranz):
			result[a].append([[random.randint(1,3),random.randint(1,vortragsanz)],[random.randint(1,3),random.randint(1,vortragsanz)]])
	return result
def sinnvollstart(original,anz):
	result=[]
	for a in range(anz):
		result.append([])
		for b in range(schueleranz):
			result[a].append([[random.randint(1,3),original[b][0]],[random.randint(1,3),original[b][1]]])
			if random.random()<0.3:
				result[a][b][0][1]=random.randint(1,vortragsanz)
			if random.random()<0.3:
				result[a][b][1][1]=random.randint(1,vortragsanz)
	return result
def fitness(gene):
	fitlist=[]
	gencount=0
	for s in gene:
		fitlist.append(0)
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
				fitlist[gencount]+=10000
			scount+=1	
		vcount=0
		for a in vschuel:
			zfcount=0
			for b in a:
				zfcount+=1
				if b>maxSinZFproV:
					fitlist[gencount]+=(10000+(b-maxSinZFproV)*10000)
				elif b<minSinZFproV and b!=0:
					fitlist[gencount]+=10000
				elif b!=0 and not (zfcount in vortragsperfekt[vcount]):
					fitlist[gencount]+=10000
			vcount+=1
		gencount+=1	
	return fitlist
def createnewgens(gene,fitlist):
	newgene=[]
	superlist=[]
	count=0
	for a in gene:
		superlist.append([fitlist[count],a])
		count+=1
	superlist.sort()
	gcount=0
	for a in gene:
		mymutrate=random.random()*maxmutrate
		tmp=weighted_choice(dieweights)
		choose1=superlist[tmp][1]
		second=weighted_choice(dieweights)
		while second==tmp:  #stellt sicher, dass das selbe gen nicht zwei mal ausgewählt wird
			second=weighted_choice(dieweights)
		choose2=superlist[second][1]
		newgene.append([])
		for b in range(schueleranz):
			newgene[gcount].append([[],[]])
			for c in range(4):
				if c==0:
					tp1=0
					tp2=0
				if c==1:
					tp1=0
					tp2=1
				if c==2:
					tp1=1
					tp2=0
				if c==3:
					tp1=1
					tp2=1
				if random.random()<mymutrate:
					newgene[gcount][b][tp1].append(random.randint(1,3))
				else:
					if random.random()<0.5:
						newgene[gcount][b][tp1].append(choose1[b][tp1][tp2])
					else:
						newgene[gcount][b][tp1].append(choose2[b][tp1][tp2])
		gcount+=1
	return newgene
def geneticsearch():
	generation=0
	tmp=100000000
	gene=sinnvollstart(schuelerperfekt,genanz)
	while tmp>0:
		fitnesses=fitness(gene)
		tmp=min(fitnesses)
		print ("bestfitness: "+str(tmp)+"   generation:"+str(generation))
		gene=createnewgens(gene,fitnesses)
		generation+=1
	bestgen=gene[fitnesses.index(min(fitnesses))]
geneticsearch()
print (int(round(time.time() * 1000))-millis)