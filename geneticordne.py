#vortragsperfekt: mehrdimensionale liste mit zeitfensterdaten
#schuelerperfekt: mehrdimensionale liste mit gewählten vortragen
#genarray: jeder schüler als einzelner array, pro schüler zwei arrays mit je einem vortrag und einem Zeitfenster
superminuswert=0
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
font=pygame.font.Font(None,15)
pygame.draw.line(screen,[0,0,0],[800,scheight-175],[800,scheight-5])
pygame.draw.line(screen,[0,0,0],[800,scheight-5],[scwidth-100,scheight-5])
text=font.render("fitness",1,(0,0,0))
screen.blit(text,[780,scheight-195])
text=font.render("generation",1,(0,0,0))
screen.blit(text,[scwidth-90,scheight-15])
schuelerperfekt=[]
vortragsperfekt=[]
alltimeentwick=[]
millis = int(round(time.time() * 1000))
levelofdo=0
mode=0
minSinZFproV=5
maxSinZFproV=25
vortragsanz=67
schueleranz=320
genanz=1000
maxmutrate=0.015
supermutationrate=0.01
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
def drawgen(gen,bfit,generation,allfit):
	global superminuswert
	global mode
	global alltimeentwick
	alltimeentwick.append(bfit)
	allfit.sort()
	font=pygame.font.Font(None,20)
	for event in pygame.event.get():
		if event.type == pygame.MOUSEBUTTONDOWN:
			if event.pos[0]>10 and event.pos[0]<140 and event.pos[1]>scheight-200 and event.pos[1]<scheight-170:
				if mode==0:
					mode=1
				elif mode==1:
					mode=2
				elif mode==2:
					mode=0
		if event.type == pygame.MOUSEBUTTONUP:
			None 
	pygame.draw.rect(screen,[255,255,255],[0,0,scwidth,scheight-200],0)
	pygame.draw.rect(screen,[255,255,255],[0,scheight-200,700,200],0)
	pygame.draw.rect(screen,[33,33,33],[10,scheight-200,130,30],1)
	if mode==0:
		text=font.render("Top Gen List",1,(0,0,0))
		screen.blit(text,[40,scheight-190])
	if mode==1:
		text=font.render("All Time Fitness",1,(0,0,0))
		screen.blit(text,[20,scheight-190])
		left=0
		top=0
		for a in allfit:
			text=font.render(str(a),1,(0,0,0))
			screen.blit(text,[left,top])
			left+=100
			if left>=scwidth-10:
				left=0
				top+=20
				if top>680:
					break
	if mode==2:
		text=font.render("Netstructure",1,(0,0,0))
		screen.blit(text,[40,scheight-190])
		pygame.draw.line(screen,[0,0,0],[10,30],[10,690])
		pygame.draw.line(screen,[0,0,0],[10,690],[scwidth-80,690])
		text=font.render("fitness",1,(0,0,0))
		screen.blit(text,[5,10])
		text=font.render("generation",1,(0,0,0))
		screen.blit(text,[scwidth-70,680])
		all=0
		for a in alltimeentwick:
			all+=a
		avg=all//len(alltimeentwick)
		einpfit=avg/330
		einpgen=len(alltimeentwick)/(scwidth-90)
		count=0
		lastpos=[]
		for a in alltimeentwick:
			if int(690-a/einpfit)<0:
				rintu=0
			else:
				rintu=int(690-a/einpfit)
			pygame.draw.rect(screen,[255,0,0],[int(10+count/einpgen),rintu,1,1],1)
			if lastpos:
				pygame.draw.line(screen,[255,0,0],lastpos,[int(10+count/einpgen),rintu])
			lastpos=[int(10+count/einpgen),rintu]
			count+=1
	if mode==0:
		left=0
		top=0
		for a in range(schueleranz):
			pygame.draw.rect(screen,[255,0,0],[left,top,10,10],0)
			left+=20
			if left>=scwidth-10:
				left=0
				top+=20
	left=0
	top=700
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
			vschuel[z[0]-1][z[1]-1]+=1
	font=pygame.font.Font(None,20)
	gewaehlt=[]
	for a in range(vortragsanz):
		gewaehlt.append(0)
	for a in schuelerperfekt:
		for b in a:
			gewaehlt[b-1]+=1
	szffail=0
	sdoublev=0
	upwahlen=0
	drwahlen=0
	for a in gen:
		for z in a:
			if z[1]!=schuelerperfekt[count][0] and z[1]!=schuelerperfekt[count][1]:
				if z[1]!=schuelerperfekt[count][2]:
					upwahlen+=1
				else:
					drwahlen+=1
		if a[0][0]==a[1][0]:
			sdoublev+=1
		if a[0][1]==a[1][1]:
			szffail+=1
		if mode==0:
			startpos=[5+(count*20)%(scwidth),5+((count*20)//(scwidth))*20]
			endpos=[7+((a[0][0]-1)*25)%(scwidth-10),scheight-293+((a[0][0]*25)//(scwidth-10))*25]
			if a[0][1]==1:
				color=[0,0,0]
			if a[0][1]==2:
				color=[0,255,0]
			if a[0][1]==3:
				color=[255,0,255]
			pygame.draw.line(screen,color,startpos,endpos)
			endpos=[7+((a[1][0]-1)*25)%(scwidth-10),scheight-293+((a[1][0]*25)//(scwidth-10))*25]
			if a[1][1]==1:
				color=[0,0,0]
			if a[1][1]==2:
				color=[0,255,0]
			if a[1][1]==3:
				color=[255,0,255]
			pygame.draw.line(screen,color,startpos,endpos)
		count+=1
	vcount=0
	belegtevortr=0
	zuklein=0
	zfpasstnicht=0
	dreier=0
	for a in vschuel:
		text=font.render(str(a[0]),1,(0,0,0))
		screen.blit(text,[vcount*25,scheight-283])
		text=font.render(str(a[1]),1,(0,255,0))
		screen.blit(text,[vcount*25,scheight-263])
		text=font.render(str(a[2]),1,(255,0,255))
		screen.blit(text,[vcount*25,scheight-243])
		pygame.draw.line(screen,[100,100,100],[0,scheight-228],[scwidth,scheight-228])
		text=font.render(str(gewaehlt[vcount]),1,(255,0,0))
		screen.blit(text,[vcount*25,scheight-223])
		if a[0]>0:
			if not (1 in vortragsperfekt[vcount]):
				zfpasstnicht+=1
			belegtevortr+=1
			if a[0]<5:
				zuklein+=1
		if a[1]>0:
			if not (2 in vortragsperfekt[vcount]):
				zfpasstnicht+=1
			belegtevortr+=1
			if a[1]<5:
				zuklein+=1
		if a[2]>0:
			if not (3 in vortragsperfekt[vcount]):
				zfpasstnicht+=1
			belegtevortr+=1
			if a[2]<5:
				zuklein+=1
		if a[0]>0 and a[1]>0 and a[2]>0:
			dreier+=1
		vcount+=1
	text=font.render("Schueler zwei mal im selben ZF: "+str(szffail),1,(0,0,0))
	screen.blit(text,[400,scheight-153])
	text=font.render("Schueler zwei mal im selben Vortrag: "+str(sdoublev),1,(0,0,0))
	screen.blit(text,[400,scheight-123])
	text=font.render("vortrags die in drei ZFs gehalten werden: "+str(dreier),1,(0,0,0))
	screen.blit(text,[400,scheight-93])
	text=font.render("schueler in unpassendem vortrag: "+str(upwahlen),1,(0,0,0))
	screen.blit(text,[400,scheight-63])
	text=font.render("schueler in drittwahl: "+str(drwahlen),1,(0,0,0))
	screen.blit(text,[400,scheight-33])
	text=font.render("vortrags in unpassenden zfs: "+str(zfpasstnicht),1,(0,0,0))
	screen.blit(text,[10,scheight-153])
	text=font.render("Zeitfenster mit zu wenig Teilnehmern: "+str(zuklein),1,(0,0,0))
	screen.blit(text,[10,scheight-123])
	text=font.render("Belegte Zeitfenster: "+str(belegtevortr),1,(0,0,0))
	screen.blit(text,[10,scheight-93])
	text=font.render("generation: "+str(generation),1,(0,0,0))
	screen.blit(text,[10,scheight-63])
	text=font.render("bestfitness: "+str(bfit),1,(0,0,0))
	screen.blit(text,[10,scheight-33])
	pygame.draw.rect(screen,[255,0,0],[800+generation-superminuswert,scheight-5-bfit//10,1,1],1)
	if superminuswert==0:
		pygame.draw.rect(screen,[255,0,0],[800+generation,scheight-5-bfit//1000000,1,1],1)
	else:
		if generation-superminuswert>=1000:
			pygame.draw.rect(screen,[255,255,255],[700,scheight-199,scwidth-700,199],0)
			pygame.draw.line(screen,[0,0,0],[800,scheight-175],[800,scheight-5])
			pygame.draw.line(screen,[0,0,0],[800,scheight-5],[scwidth-100,scheight-5])
			text=font.render("fitness",1,(0,0,0))
			screen.blit(text,[780,scheight-195])
			text=font.render("generation",1,(0,0,0))
			screen.blit(text,[scwidth-90,scheight-15])
			superminuswert+=1000
	if bfit<1000000 and superminuswert==0:
		pygame.draw.rect(screen,[255,255,255],[700,scheight-199,scwidth-700,199],0)
		superminuswert=generation
		pygame.draw.line(screen,[0,0,0],[800,scheight-175],[800,scheight-5])
		pygame.draw.line(screen,[0,0,0],[800,scheight-5],[scwidth-100,scheight-5])
		text=font.render("fitness",1,(0,0,0))
		screen.blit(text,[780,scheight-195])
		text=font.render("generation",1,(0,0,0))
		screen.blit(text,[scwidth-90,scheight-15])
		alltimeentwick=[]
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
			a1=random.randint(1,vortragsanz)
			b1=random.randint(1,vortragsanz)
			a2=random.choice(vortragsperfekt[a1-1])
			tmp=vortragsperfekt[b1-1][:]
			if a2 in tmp:
				tmp.remove(a2)
			if tmp:
				b2=random.choice(tmp)
			else:
				b2=random.choice(vortragsperfekt[b1-1])
			result[a].append([[a1,a2],[b1,b2]])
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
	global levelofdo
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
				vschuel[z[0]-1][z[1]-1]+=1
				if z[0]!=schuelerperfekt[scount][0] and z[0]!=schuelerperfekt[scount][1]:
					if z[0]!=schuelerperfekt[scount][2]:
						fitlist[gencount]+=5
					else:
						fitlist[gencount]+=1
			if vz[0][0]==vz[1][0]:
				fitlist[gencount]+=1000000
			if vz[0][1]==vz[1][1]:
				fitlist[gencount]+=1000000
			scount+=1	
		vcount=0
		haltcount=0
		for a in vschuel:
			zfcount=0
			#if a[0]!=0 and a[1]!=0 and a[2]!=0 and a[0]+a[1]+a[2]<maxSinZFproV*2:
			#	vcount+=1
			#	fitlist[gencount]+=8*1000000+500*min(a[0],a[1],a[2])
			#	continue
			for b in a:
				zfcount+=1
				if b!=0:
					haltcount+=1
					if not (zfcount in vortragsperfekt[vcount]):
						fitlist[gencount]+=1000000+b*500
						continue
					if levelofdo>0:
						if b>maxSinZFproV:
							fitlist[gencount]+=(levelofdo+(b-maxSinZFproV)*levelofdo)
						if b<minSinZFproV and b!=0:
							fitlist[gencount]+=b*levelofdo
			vcount+=1 
		if haltcount>vortragsanz:
			fitlist[gencount]+=(haltcount-vortragsanz)*levelofdo
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
		#wegmach=-1
		#if random.random()<supermutationrate:
		#	wegmach=random.randint(1,vortragsanz)
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
						newgene[gcount][b][tp1].append(random.randint(1,vortragsanz))
					else:
						tmp=vortragsperfekt[newgene[gcount][b][tp1][0]-1][:]
						if tp1==1:
							if newgene[gcount][b][0][1] in tmp:
								tmp.remove(newgene[gcount][b][0][1])
						if tmp:	
							newgene[gcount][b][tp1].append(random.choice(tmp))
						else:
							newgene[gcount][b][tp1].append(random.choice(vortragsperfekt[newgene[gcount][b][tp1][0]-1]))
				else:
					if random.random()<0.5:
						newgene[gcount][b][tp1].append(choose1[b][tp1][tp2])
					else:
						newgene[gcount][b][tp1].append(choose2[b][tp1][tp2])
				#if tp2==1 and newgene[gcount][b][tp1][1]==wegmach:
				#	newgene[gcount][b][tp1][1]=random.randint(1,vortragsanz)
		gcount+=1
	return newgene
def geneticsearch():
	global levelofdo
	generation=0
	tmp=100000000
	gene=randomgens(genanz)
	while tmp>0:
		fitnesses=fitness(gene)
		bestgen=gene[fitnesses.index(min(fitnesses))]
		tmp=min(fitnesses)
		if tmp<200 and levelofdo<200:
			levelofdo+=1
		drawgen(bestgen,tmp,generation,fitnesses[:])
		print ("bestfitness: "+str(tmp)+"   generation:"+str(generation))
		gene=createnewgens(gene,fitnesses)
		generation+=1
geneticsearch()
print (int(round(time.time() * 1000))-millis)