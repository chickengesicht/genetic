#vortragsperfekt: mehrdimensionale liste mit zeitfensterdaten
#schuelerperfekt: mehrdimensionale liste mit gewählten vortragen
#genarray: jeder schüler als einzelner array, pro schüler zwei arrays mit je einem vortrag und einem Zeitfenster
x = 0
y = 20
import os
os.environ['SDL_VIDEO_WINDOW_POS'] = "%d,%d" % (x,y)
import random,time,pygame
pygame.init()
scwidth=1900
scheight=1000
screen=pygame.display.set_mode([scwidth,scheight])
screen.fill([255,255,255])
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
def drawgen(gen):
	screen.fill([255,255,255])
	left=0
	top=0
	for a in range(schueleranz):
		pygame.draw.rect(screen,[255,0,0],[left,top,10,10],0)
		left+=20
		if left>=scwidth-10:
			left=0
			top+=20
	left=0
	top=900
	for a in range(vortragsanz):
		pygame.draw.rect(screen,[0,0,255],[left,top,15,15],0)
		left+=25
		if left>=scwidth-10:
			left=0
			top+=25
	count=0
	vschuel=[]
	for a in range(vortragsanz):
		vschuel.append([0,0,0])
	for vz in gen:
		for z in vz:
			vschuel[z[1]-1][z[0]-1]+=1
	font=pygame.font.Font(None,20)
	for a in gen:
		startpos=[5+(count*20)%(scwidth),5+((count*20)//(scwidth))*20]
		endpos=[7+((a[0][1]-1)*25)%(scwidth-10),scheight-93+((a[0][1]*25)//(scwidth-10))*25]
		if a[0][0]==1:
			color=[0,0,0]
		if a[0][0]==2:
			color=[0,255,0]
		if a[0][0]==3:
			color=[255,0,255]
		pygame.draw.line(screen,color,startpos,endpos)
		endpos=[7+((a[1][1]-1)*25)%(scwidth-10),scheight-93+((a[1][1]*25)//(scwidth-10))*25]
		if a[1][0]==1:
			color=[0,0,0]
		if a[1][0]==2:
			color=[0,255,0]
		if a[1][0]==3:
			color=[255,0,255]
		pygame.draw.line(screen,color,startpos,endpos)
		count+=1
	vcount=0
	for a in vschuel:
		text=font.render(str(a[0]),1,(0,0,0))
		screen.blit(text,[vcount*25,scheight-73])
		text=font.render(str(a[1]),1,(0,255,0))
		screen.blit(text,[vcount*25,scheight-53])
		text=font.render(str(a[2]),1,(255,0,255))
		screen.blit(text,[vcount*25,scheight-33])
		vcount+=1
	pygame.display.flip()
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
					if tp2==0:
						newgene[gcount][b][tp1].append(random.randint(1,3))
					else:
						newgene[gcount][b][tp1].append(random.randint(1,vortragsanz))
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
		bestgen=gene[fitnesses.index(min(fitnesses))]
		drawgen(bestgen)
		tmp=min(fitnesses)
		print ("bestfitness: "+str(tmp)+"   generation:"+str(generation))
		gene=createnewgens(gene,fitnesses)
		generation+=1
geneticsearch()
print (int(round(time.time() * 1000))-millis)