import numpy,sys,math,copy
import random
import matplotlib.pyplot as plotting
class node(object):
	def __init__(self,number,indices):
		self.number=number
		self.medn=-1
		self.left=None
		self.right=None
		self.leaflabel=-1
		self.examples=indices
		self.maxclass=-1
		self.test=[]
		self.id=-1
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
numnodes=0
def generatetree(part,depth,numnode):
	#print "----------------"
	#print depth
	# if(depth>=2):
	# 	return
	
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
		part.id=numnode[0]
		numnode[0]=numnode[0]+1
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
	part.id=numnode[0]
	numnode[0]=numnode[0]+1
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
	generatetree(leftnode,depth+1,numnode)
	part.left=leftnode

	rightnode=node(0,rightindex)
	generatetree(rightnode,depth+1,numnode)
	part.right=rightnode

	

generatetree(root,0,[0])
print "tree created"

numnodes=0
def getnodes(no):
	if(not no):
		#print "returning 0"
		return 0
	if(no.leaflabel!=-1):
		return 1
	else:
		return 1+getnodes(no.left)+getnodes(no.right)


numnodes=getnodes(root)
print numnodes



def search(searchnode,vals,indx):
	if(searchnode.leaflabel!=-1):
		return searchnode.leaflabel
	attindex=searchnode.number
	attvalue=vals[attindex]
	searchnode.test.append(indx)
	if(attindex<10):
		if(attvalue<=searchnode.medn):
			return search(searchnode.left,vals,indx)
		else:
			return search(searchnode.right,vals,indx)
	else:
		if(attvalue==0):
			return search(searchnode.left,vals,indx)
		else:
			return search(searchnode.right,vals,indx)

	


#Tree learning complete


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


# finaldata2=[]
# finalans2=[]
# testfile2=open("test2.dat","r")
# nn2=testfile2.readline()
# for line2 in testfile2:
# 	testval2=line2.split(",")
# 	xnew2=[]
# 	for y2 in range(0,numattrs):
# 		xnew2.append(int(testval2[y]))
# 	finaldata2.append(xnew2)
# 	finalans2.append(int(testval2[numattrs]))

# total2=len(finalans2)








#pruning
testing=[]
nums=0
total=len(finaldata)
def accuracy(root):
	count=0
	for i in range(0,total):
		xnew=finaldata[i]
		testans=search(root,xnew,i)
		testing.append(testans)
		if(testans==finalans[i]):
			count=count+1
	acc=(count*100.0)/total
	return acc



def accuracy2(root):
	count=0
	for i in range(0,total):
		xnew=finaldata[i]
		testans=search(root,xnew,i)
		
		if(testans==finalans[i]):
			count=count+1
	acc=(count*100.0)/total
	return acc


def accuracy3(root):
	count2=0
	for i in range(0,total2):
		xnew2=finaldata2[i]
		testans2=search(root,xnew2,i)
		
		if(testans2==finalans2[i]):
			count2=count2+1
	acc2=(count2*100.0)/total2
	return acc2

print "init",
initacc= accuracy(root)
print initacc

# print root.left.right.number
# print len(root.left.right.examples)
# print len(root.left.right.test)

def changeinaccuracy(nodetocheck,val):
	change=0
	ind=nodetocheck.test
	#print nodetocheck.leaflabel
	numex=len(ind)
	for u in ind:
		xx=finaldata[u]
		
		
		if(testing[u]!=val):
			if(val==finalans[u]):
				change=change+1
			elif(testing[u]==finalans[u]):
				change=change-1
	if(change<3):
		change=0
	delta= (change*1.0)/total
	#print delta
	return delta



def prune(prunenode,reqnode,maxacc,depth):
	
	#makingcopy=copy.deepcopy(prunenode)
	if(prunenode==None):
		return 
	if(prunenode.leaflabel!=-1):
		#print "leaf found"
		return 
	#print depth
	prune(prunenode.left,reqnode,maxacc,depth+1)
	prune(prunenode.right,reqnode,maxacc,depth+1)
	
		#print "pruning",
		#print prunenode.number
	#if(depth>10):
	prunenode.leaflabel=prunenode.maxclass
	# save1=prunenode.left
	# save2=prunenode.right
	# prunenode.left=None
	# prunenode.right=None
	#topcopy=copy.deepcopy(top)
	ans=changeinaccuracy(prunenode,prunenode.leaflabel)

	#print ans
	#top=copy.deepcopy(topcopy)
	if(ans>maxacc[0]):
		#print ans
		reqnode[0]=prunenode
		maxacc[0]=ans
		#print maxacc[0]
		#print "depth",depth

	prunenode.leaflabel=-1
	# prunenode.left=save1
	# prunenode.left=save2







# acc=[0.0]
# prunestep=0
# flag=False
# i=0
# while(acc[0]!=0 or flag==False):
# 	flag=True
# 	prunestep=prunestep+1
# 	best=[node(0,[])]
#  	#savingroot=copy.deepcopy(root)
	
# 	prune(root,best,acc,0)
# 	#print getnodes(root)
# 	best[0].leaflabel=best[0].maxclass
# 	print acc[0]
# 	initacc=initacc+acc[0]
# 	print initacc
# 	print "***********"
numbs=initacc
counter=0


xd=[]
yd=[]
yd2=[]

visited=[]
while(counter<2000):
	print counter
	counter=counter+1
	#print getnodes(root)
	acc=[0]
	best=[node(0,[])]
	prune(root,best,acc,0)
	#print len(best[0].examples)
	#print best[0].number
	#print len(best[0].examples)
	#print getnodes(best[0])
	# print counter
	# print best[0].id
	if(best[0].id in visited):
		#print best[0].id
		break
	else:
		visited.append(best[0].id)
	best[0].leaflabel=best[0].maxclass
	best[0].left=None
	best[0].right=None
	# if(acc[0]==0):
	# 	break
	# if(acc[0]<0.001):
	# 	break
	# numbs=numbs+acc[0]
	# ac=accuracy2(root)
	# ac2=accuracy2(root)
	# print getnodes(root)
	# print numbs
	# print("----------")
	#print len(visited)

	#print numbs
	# xd.append(numnodes-len(visited))
	# yd.append(ac)
	# yd2.append(ac2)


#print visited
# print numbs
# finalnodes=numnodes-len(visited)

finalacc= accuracy(root)
print finalacc

# print xd
# print yd
# xd.append(finalnodes)
# yd.append(finalacc)
# plotting.figure(0)
# plotting.plot(xd,yd)
# plotting.xlabel('Number of nodes', fontsize=18)
# plotting.ylabel('Accuracy', fontsize=16)
# plotting.savefig("valid.jpg",dpi=72)
# plotting.show()


# plotting.figure(1)
# plotting.plot(xd,yd2)
# plotting.xlabel('Number of nodes', fontsize=18)
# plotting.ylabel('Accuracy', fontsize=16)
# plotting.savefig("test.jpg",dpi=72)
# plotting.show()





# print root.number
# print len(root.examples)
# print root.leaflabel
# print root.left.number
# while(root.left!=None):
# 	print root.left.number
# 	root=root.left
# print getnodes(root)
# acc=[0]
# prune(root,best,acc,0)
# best[0].leaflabel=best[0].maxclass
# best[0].left=None
# best[0].right=None
# print len(best[0].examples)
# print best[0].number
# print("----------")
# print getnodes(root)
# acc=[0]
# prune(root,best,acc,0)
# best[0].leaflabel=best[0].maxclass
# best[0].left=None
# best[0].right=None
# print len(best[0].examples)
# print best[0].number
# print getnodes(root)














