#vortragsperfekt: mehrdimensionale liste mit zeitfensterdaten [[v1,v2,v3],[v1,v2,v3]]
#schuelerperfekt: mehrdimensionale liste mit gewählten vortragen
#genarray: jeder schüler als einzelner array, pro schüler zwei arrays mit einer zahl die Vortrag und Zeitfenster angibt 
superminuswert=0
x = 0
y = 20
import os
os.environ['SDL_VIDEO_WINDOW_POS'] = "%d,%d" % (x,y)
from multiprocessing import Process,Queue
import random,time,pygame,multiprocessing
import schuelerp,vortragp
schuelerperfekt=schuelerp.getsperfekt()
vortragsperfekt=vortragp.getvperfekt()
print (schuelerperfekt)
print ("\n\n")
print (vortragsperfekt)
pygame.init()
scwidth=1900
scheight=1000
screen=pygame.display.set_mode([scwidth,scheight])
screen.fill([255,255,255])
font=pygame.font.Font(None,15)
alltimeentwick=[]
worstentwick=[]
allemoeglich=[]
randomtest=[]
millis = int(round(time.time() * 1000))
levelofdo=0
mode=0
minSinZFproV=5
maxSinZFproV=25
vortragsanz=len(vortragsperfekt)
schueleranz=len(schuelerperfekt)
genanz=1000
maxmutrate=0.005
supermutationrate=0.01
holdvari=3000
dieweights=[]
gewaehlt=[]
for a in range(vortragsanz):
	gewaehlt.append(0)
for a in schuelerperfekt:
	for b in a:
		if b>=0:
			gewaehlt[b]+=1
for a in range(genanz):
	dieweights.append(60.0/(a+3))   #probability function
#for a in range(schueleranz):  #zufällige wahlen zu testzwecken
#	schuelerperfekt.append([random.randint(0,vortragsanz-1),random.randint(0,vortragsanz-1),random.randint(0,vortragsanz-1)])
"""for a in range(vortragsanz):
	rin=[random.randint(0,2)]
	for c in range(4):
		b=random.randint(0,2)
		if not(b in rin):
			rin.append(b)
	vortragsperfekt.append(rin)"""
vcount=0
for a in vortragsperfekt:
	for b in a:
		allemoeglich.append(vcount*3+b)
		randomtest.append(0)
	vcount+=1
def drawgen(gen,bfit,worstfit,generation,allfit):
	global superminuswert
	global mode
	global alltimeentwick,worstentwick
	global gewaehlt
	alltimeentwick.append(bfit)
	allfit.sort()
	worstentwick.append(worstfit)
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
			if event.pos[0]>scwidth-150 and event.pos[0]<scwidth-20 and event.pos[1]>scheight-50 and event.pos[1]<scheight-20:
				with open("verteilung.txt","w") as infile:
					wcount=1
					for a in gen:
						infile.write(str(wcount)+": "+str((a[0]//3)+1)+" - "+str((a[0]%3)+1)+" ; "+str((a[1]//3)+1)+" - "+str((a[1]%3)+1)+" :: gewaehlt wurde "+str(schuelerperfekt[wcount-1][0]+1)+" - "+str(schuelerperfekt[wcount-1][1]+1)+" - "+str(schuelerperfekt[wcount-1][2]+1)+" \n")
						wcount+=1
		if event.type == pygame.MOUSEBUTTONUP:
			None 
	screen.fill([255,255,255])
	pygame.draw.rect(screen,[33,33,33],[scwidth-150,scheight-50,130,30],1)
	text=font.render("Write Distribution",1,(0,0,0))
	screen.blit(text,[scwidth-120,scheight-40])
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
		count=0
		lastpos=[]
		einpgen=len(worstentwick)/(scwidth-90)
		for a in worstentwick:
			if int(690-a/einpfit)<0:
				rintu=0
			else:
				rintu=int(690-a/einpfit)
			pygame.draw.rect(screen,[0,0,255],[int(10+count/einpgen),rintu,1,1],1)
			if lastpos:
				pygame.draw.line(screen,[0,0,255],lastpos,[int(10+count/einpgen),rintu])
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
		font=pygame.font.Font(None,15)
		text=font.render(str(a+1),1,(255,255,255))
		screen.blit(text,[left,top])
		left+=25
		if left>=scwidth-10:
			left=800
			top+=150
	count=0
	vschuel=[]
	for a in range(vortragsanz):
		vschuel.append([0,0,0])
	for vz in gen:
		for z in vz:
			vschuel[z//3][z%3]+=1
	font=pygame.font.Font(None,20)
	szffail=0
	sdoublev=0
	upwahlen=0
	drwahlen=0
	for a in gen:
		for z in a:
			if z//3!=schuelerperfekt[count][0] and z//3!=schuelerperfekt[count][1]:
				if z//3!=schuelerperfekt[count][2]:
					upwahlen+=1
				else:
					drwahlen+=1
		if a[0]//3==a[1]//3:
			sdoublev+=1
		if a[0]%3==a[1]%3:
			szffail+=1
		if mode==5:
			startpos=[5+(count*20)%(scwidth),5+((count*20)//(scwidth))*20]
			endpos=[7+((a[0]//3)*25)%(scwidth-10),scheight-293+(((a[0]//3)*25)//(scwidth-10))*25]
			if a[0]%3==0:
				color=[0,0,0]
			if a[0]%3==1:
				color=[0,255,0]
			if a[0]%3==2:
				color=[255,0,255]
			pygame.draw.line(screen,color,startpos,endpos)
			endpos=[7+((a[1]//3)*25)%(scwidth-10),scheight-293+(((a[1]//3)*25)//(scwidth-10))*25]
			if a[1]%3==0:
				color=[0,0,0]
			if a[1]%3==1:
				color=[0,255,0]
			if a[1]%3==2:
				color=[255,0,255]
			pygame.draw.line(screen,color,startpos,endpos)
		count+=1
	vcount=0
	belegtevortr=0
	zuklein=0
	zfpasstnicht=0
	dreier=0
	doppelt=0
	for a in vschuel:
		if vcount*25<scwidth-10:
			hextra=0
			wteil=vcount*25
		else:
			hextra=150
			wteil=800+vcount*25-scwidth
		text=font.render(str(a[0]),1,(0,0,0))
		screen.blit(text,[wteil,hextra+scheight-283])
		text=font.render(str(a[1]),1,(0,255,0))
		screen.blit(text,[wteil,hextra+scheight-263])
		text=font.render(str(a[2]),1,(255,0,255))
		screen.blit(text,[wteil,hextra+scheight-243])
		if hextra==0:
			pygame.draw.line(screen,[100,100,100],[0,scheight-228],[scwidth,scheight-228])
		text=font.render(str(gewaehlt[vcount]),1,(255,0,0))
		screen.blit(text,[wteil,hextra+scheight-223])
		if a[0]>0:
			if not (0 in vortragsperfekt[vcount]):
				zfpasstnicht+=1
			belegtevortr+=1
			if a[0]<5:
				zuklein+=1
		if a[1]>0:
			if not (1 in vortragsperfekt[vcount]):
				zfpasstnicht+=1
			belegtevortr+=1
			if a[1]<5:
				zuklein+=1
		if a[2]>0:
			if not (2 in vortragsperfekt[vcount]):
				zfpasstnicht+=1
			belegtevortr+=1
			if a[2]<5:
				zuklein+=1
		if a[0]>0 and a[1]>0 and a[2]>0:
			dreier+=1
		if gewaehlt[vcount]<maxSinZFproV:
			if (a[0]>0 and a[1]>0) or (a[1]>0 and a[2]>0) or (a[0]>0 and a[2]>0):
				doppelt+=1
		vcount+=1
	text=font.render("Vortrags in zwei ZF unter "+str(maxSinZFproV)+" anwahlen: "+str(doppelt),1,(0,0,0))
	screen.blit(text,[400,scheight-153])
	text=font.render("Schueler zwei mal im selben Vortrag: "+str(sdoublev),1,(0,0,0))
	screen.blit(text,[400,scheight-123])
	text=font.render("vortrags die in drei ZFs gehalten werden: "+str(dreier),1,(0,0,0))
	screen.blit(text,[400,scheight-93])
	text=font.render("schueler in unpassendem vortrag: "+str(upwahlen),1,(0,0,0))
	screen.blit(text,[400,scheight-63])
	text=font.render("schueler in drittwahl: "+str(drwahlen),1,(0,0,0))
	screen.blit(text,[400,scheight-33])
	text=font.render("maxmutrate: "+str(maxmutrate),1,(0,0,0))
	screen.blit(text,[10,scheight-153])
	text=font.render("Zeitfenster mit zu wenig Teilnehmern: "+str(zuklein),1,(0,0,0))
	screen.blit(text,[10,scheight-123])
	text=font.render("Belegte Zeitfenster: "+str(belegtevortr),1,(0,0,0))
	screen.blit(text,[10,scheight-93])
	text=font.render("generation: "+str(generation),1,(0,0,0))
	screen.blit(text,[10,scheight-63])
	text=font.render("bestfitness: "+str(bfit),1,(0,0,0))
	screen.blit(text,[10,scheight-33])
	if bfit<1000000 and superminuswert==0:
		superminuswert=generation
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
			a1=random.choice(allemoeglich)
			b1=random.choice(allemoeglich)
			while b1%3==a1%3 or b1//3==a1//3:
				b1=random.choice(allemoeglich)
			result[a].append([a1,b1])
	return result
"""def sinnvollstart(original,anz):
	result=[]
	for a in range(anz):
		result.append([])
		for b in range(schueleranz):
			result[a].append([[random.randint(1,3),original[b][0]],[random.randint(1,3),original[b][1]]])
			if random.random()<0.3:
				result[a][b][0][1]=random.randint(1,vortragsanz)
			if random.random()<0.3:
				result[a][b][1][1]=random.randint(1,vortragsanz)
	return result"""
def fitness(gene):
	global levelofdo,gewaehlt
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
				vschuel[z//3][z%3]+=1
				if (schuelerperfekt[scount][0]==-1 and schuelerperfekt[scount][1]==-1 and schuelerperfekt[scount][2]==-1):
					continue
				if z//3!=schuelerperfekt[scount][0] and z//3!=schuelerperfekt[scount][1]:
					if z//3!=schuelerperfekt[scount][2]:
						fitlist[gencount]+=5
					else:
						fitlist[gencount]+=1
			if vz[0]//3==vz[1]//3:
				fitlist[gencount]+=1000000
			if vz[0]%3==vz[1]%3:
				fitlist[gencount]+=1000000
			scount+=1	
		vcount=0
		haltcount=0
		for a in vschuel:
			zfcount=0
			minintr=-1
			if gewaehlt[vcount]<maxSinZFproV:
				if a[0]>0 and a[1]>0:
					minintr=a.index(min(a[0],a[1]))
					fitlist[gencount]+=min(a[0],a[1])*levelofdo
				if a[0]>0 and a[2]>0:
					minintr=a.index(min(a[0],a[2]))
					fitlist[gencount]+=min(a[0],a[2])*levelofdo
				if a[1]>0 and a[2]>0:
					minintr=a.index(min(a[1],a[2]))
					fitlist[gencount]+=min(a[1],a[2])*levelofdo
			elif gewaehlt[vcount]<2*maxSinZFproV and a[0]>0 and a[1]>0 and a[2]>0:
				minintr=a.index(min(a))
				fitlist[gencount]+=min(a)*levelofdo
			for b in a:
				if b!=0:
					haltcount+=1
					if not (zfcount in vortragsperfekt[vcount]):
						fitlist[gencount]+=1000000+b*500
						continue
					if levelofdo>0:
						if b>maxSinZFproV:
							fitlist[gencount]+=(levelofdo+(b-maxSinZFproV)*levelofdo)
						if zfcount!=minintr:
							if b<minSinZFproV:
								if gewaehlt[vcount]>4 and b==max(a):
									fitlist[gencount]+=(5-b)*levelofdo
								else:
									fitlist[gencount]+=b*levelofdo
				zfcount+=1
			vcount+=1 
		gencount+=1	
	return fitlist
def multifit(gene):
	cpus=multiprocessing.cpu_count()
	q=Queue()
	anzpro=len(gene)//(cpus-1)
	uber=len(gene)-anzpro*(cpus-1)
	runlen=[]
	for a in range(cpus-1):
		runlen.append(anzpro)
		if uber>0:
			runlen[a]+=1
			uber-=1
	wert=0
def createnewgens(gene,fitlist):
	newgene=[]
	superlist=[]
	count=0
	for a in gene:
		superlist.append([fitlist[count]+random.random(),a])
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
			for c in range(2):
				if random.random()<mymutrate:
					if c==0:
						newgene[gcount][b][c]=random.choice(allemoeglich)
					else:
						tmp=random.choice(allemoeglich)
						while tmp%3==newgene[gcount][b][0]%3 or tmp//3==newgene[gcount][b][0]//3:
							tmp=random.choice(allemoeglich)
						newgene[gcount][b][c]=tmp
						
				else:
					if c==0:
						if random.random()<0.5:
							newgene[gcount][b][c]=choose1[b][c]
						else:
							newgene[gcount][b][c]=choose2[b][c]
					else:
						if random.random()<0.5:
							newgene[gcount][b][c]=choose1[b][c]
						else:
							newgene[gcount][b][c]=choose2[b][c]
						while newgene[gcount][b][c]%3==newgene[gcount][b][0]%3 or newgene[gcount][b][c]//3==newgene[gcount][b][0]//3:
							newgene[gcount][b][c]=random.choice(allemoeglich)
		gcount+=1
	return newgene
def geneticsearch():
	global levelofdo
	global holdvari
	generation=0
	tmp=100000000
	gene=randomgens(genanz)
	while tmp>0:
		fitnesses=fitness(gene)
		bestgen=gene[fitnesses.index(min(fitnesses))]
		tmp=min(fitnesses)
		if generation>holdvari:
			levelofdo+=1;
			holdvari+=3000;
		drawgen(bestgen[:],tmp,max(fitnesses),generation,fitnesses[:])
		print ("bestfitness: "+str(tmp)+"   generation:"+str(generation))
		#print (randomtest)
		for a in range(len(randomtest)):
			randomtest[a]=0
		gene=createnewgens(gene,fitnesses)
		generation+=1
geneticsearch()
print (int(round(time.time() * 1000))-millis)