import numpy,sys,math
import random
import matplotlib.pyplot as plotting
class node(object):
	def __init__(self,number,indices):
		self.number=number
		self.medn=-1
		self.left=None
		self.right=None
		self.leaflabel=-1
		self.maxclass=-1
		self.examples=indices
	def insertleft(self,number,indices):
		self.left=node(number,indices)
	def insertright(self,number,indices):
		self.right=node(number,indices)
	def putleft(self,leftnode):
		self.left=leftnode
	def putright(self,rightnode):
		self.right=rightnode
	def makeleaf(self,val):
		self.leaflabel=val



datafile=open("train.dat",'r')
types= datafile.readline().split(",")
x=len(types)
numattrs=x-1
data=[]
label=[]
size=0

used=[]
for i in range(0,x):
	used.append(0)

for line in datafile:
	size=size+1
	temp1=list()
	readings=line.split(",")
	for i in range(0,x-1):
		temp1.append(int(readings[i]))
	data.append(temp1)
	label.append(int(readings[x-1].strip('\n')))

initindex=[]
for i in range(0,size):
	initindex.append(i)
print size

root=node(0,initindex)
depth=0



count=0
total=0
finaldata=[]
finalans=[]
testfile=open("test.dat","r")
nn=testfile.readline()
for line in testfile:
	testval=line.split(",")
	xnew=[]
	for y in range(0,numattrs):
		xnew.append(int(testval[y]))
	finaldata.append(xnew)
	finalans.append(int(testval[numattrs]))


nums=0
total=len(finaldata)



def midsearch(searchnode,vals):
	# if(searchnode.leaflabel!=-1):
	# 	return searchnode.leaflabel
	if(searchnode.left==None and searchnode.right==None):
		return searchnode.maxclass
	
	attindex=searchnode.number
	attvalue=vals[attindex]
	if(attindex<10):
		if(attvalue<=searchnode.medn):
			if(searchnode.left!=None):
				return midsearch(searchnode.left,vals)
			else:
				return searchnode.maxclass
		else:
			if(searchnode.right!=None):
				return midsearch(searchnode.right,vals)
			else:
				return searchnode.maxclass
	else:
		if(attvalue==0):
			if(searchnode.left!=None):
				return midsearch(searchnode.left,vals)
			else:
				return searchnode.maxclass
		else:
			if(searchnode.right!=None):
				return midsearch(searchnode.right,vals)
			else:
				return searchnode.maxclass




def midaccuracy(root):
	count=0
	for i in range(0,total):
		xnew=finaldata[i]
		testans=midsearch(root,xnew)
		
		if(testans==finalans[i]):
			count=count+1
	acc=(count*100.0)/total
	return acc


def generatetree(part,depth,numnodes,start,plotxcordi,plotycordi):
	#print "----------------"
	#print depth,numnodes

	# if(depth>=2):
	# 	return
	# if(numnodes[0]%1000==0):
	# 	plotxcordi.append(numnodes[0]),plotycordi.append(midaccuracy(start[0]))
	index=part.examples
	#print len(index)
	if(not index):
		print "big"
	labels=[label[i] for i in index]
	part.maxclass=max(set(labels), key=labels.count)
	myset=set(labels)
	#print (myset)
	if(not labels):
		return
	if(len(myset)==1):
		part.leaflabel=labels[0]
		numnodes[0]=numnodes[0]+1
		return

	dataset=[data[i][:] for i in index]
	#print dataset
	sizedata=len(dataset)
	mini=0
	minval=sys.maxint
	minmedian=-1
	for i in range(0,numattrs):
		summ=0
		attrvals=[row[i] for row in dataset]
		if(i<10):
			#continous
			
			med=numpy.median(numpy.array(attrvals))
			leftarr=[0,0,0,0,0,0,0]
			rightarr=[0,0,0,0,0,0,0]
			less=[var1 for var1 in index if(data[var1][i]<=med)]
			more=[var2 for var2 in index if(data[var2][i]>med)]
			for var3 in less:
				leftarr[label[var3]-1]=leftarr[label[var3]-1]+1
			for var4 in more:
				rightarr[label[var4]-1]=rightarr[label[var4]-1]+1
			countless=sum(leftarr)
			countmore=sum(rightarr)
			
			if(countmore==0 or countmore==sizedata):
				continue
			summ1=0
			for var5 in leftarr:
				prob=(var5*1.0)/(countless)
				if(prob==0):
					continue
				summ1=summ1+(-1)*prob*(math.log(prob,2))
			summ2=0
			for var6 in rightarr:
				prob=(var6*1.0)/(countmore)
				if(prob==0):
					continue
				summ2=summ2+(-1)*prob*(math.log(prob,2))
			summ=((countless*1.0)/sizedata)*summ1+((countmore*1.0)/sizedata)*summ2
			
			
			#rint i,
			#print summ
			if(summ<minval):
				minval=summ
				mini=i
				minmedian=med
		else:
			#discrete
			leftarr=[0,0,0,0,0,0,0]
			rightarr=[0,0,0,0,0,0,0]
			less=[var1 for var1 in index if(data[var1][i]==0)]
			more=[var2 for var2 in index if(data[var2][i]==1)]

			for var3 in less:
				leftarr[label[var3]-1]=leftarr[label[var3]-1]+1
			for var4 in more:
				rightarr[label[var4]-1]=rightarr[label[var4]-1]+1
			countless=sum(leftarr)
			countmore=sum(rightarr)

			if(countmore==0 or countmore==sizedata):
				continue
			summ1=0
			for var5 in leftarr:
				prob=(var5*1.0)/(countless)
				if(prob==0):
					continue
				summ1=summ1+(-1)*prob*(math.log(prob,2))
			summ2=0
			for var6 in rightarr:
				prob=(var6*1.0)/(countmore)
				if(prob==0):
					continue
				summ2=summ2+(-1)*prob*(math.log(prob,2))
			summ=((countless*1.0)/sizedata)*summ1+((countmore*1.0)/sizedata)*summ2
			#print i,
			#print summ
			if(summ<minval):

				minval=summ
				mini=i
	#print mini
	numnodes[0]=numnodes[0]+1
	if(mini<10):
		leftindex=[ind for ind in index if data[ind][mini]<=minmedian]
		rightindex=[ind for ind in index if data[ind][mini]>minmedian]
	else:
		leftindex=[ind for ind in index if data[ind][mini]==0]
		rightindex=[ind for ind in index if data[ind][mini]==1]
	#print len(leftindex)
	#print len(rightindex)
	part.number=mini
	part.medn=minmedian
	leftnode=node(0,leftindex)
	generatetree(leftnode,depth+1,numnodes,start,plotxcordi,plotycordi)
	part.left=leftnode

	rightnode=node(0,rightindex)
	generatetree(rightnode,depth+1,numnodes,start,plotxcordi,plotycordi)
	part.right=rightnode

		
numnodes=[0]

plotxcordi=[]
plotycordi=[]
generatetree(root,0,numnodes,[root],plotxcordi,plotycordi)
print plotxcordi
print plotycordi



# def getnodes(no):
# 	if(not no):
		
# 		return 0
# 	if(no.leaflabel!=-1):
# 		return 1
# 	else:
# 		return 1+getnodes(no.left)+getnodes(no.right)


# numnodes=getnodes(root)
# print numnodes



def search(searchnode,vals):
	if(searchnode.leaflabel!=-1):
		return searchnode.leaflabel
	attindex=searchnode.number
	attvalue=vals[attindex]
	if(attindex<10):
		if(attvalue<=searchnode.medn):
			return search(searchnode.left,vals)
		else:
			return search(searchnode.right,vals)
	else:
		if(attvalue==0):
			return search(searchnode.left,vals)
		else:
			return search(searchnode.right,vals)

	


def accuracy(root):
	count=0
	for i in range(0,total):
		xnew=finaldata[i]
		testans=search(root,xnew)
		
		if(testans==finalans[i]):
			count=count+1
	acc=(count*100.0)/total
	return acc

initacc= accuracy(root)
print initacc

plotxcordi.append(numnodes[0])
plotycordi.append(initacc)


plotting.plot(plotxcordi,plotycordi)
plotting.xlabel('Number of nodes', fontsize=18)
plotting.ylabel('Accuracy', fontsize=16)
plotting.savefig("test.jpg",dpi=72)
plotting.show()






