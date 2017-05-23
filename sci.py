import numpy,sys,math
import random
from sklearn import tree


datafile=open("train.dat",'r')
types= datafile.readline().split(",")
x=len(types)
numattrs=x-1
data=[]
label=[]
size=0


for line in datafile:
	size=size+1
	temp1=list()
	readings=line.split(",")
	for i in range(0,x-1):
		temp1.append(int(readings[i]))
	data.append(temp1)
	label.append(int(readings[x-1].strip('\n')))


clf = tree.DecisionTreeClassifier(criterion='entropy',min_samples_leaf=1,min_samples_split=2,max_depth=43)
clf.fit(data,label)


count=0
total=0
testfile=open("test.dat","r")
nn=testfile.readline()
nums=0
testcase=[]
testans=[]
for line in testfile:
	total=total+1
	
	xnew=[]
	testval=line.split(",")
	for y in range(0,numattrs):
		xnew.append(int(testval[y]))
	testans.append(int(testval[x-1].strip('\n')))
	testcase.append(xnew)
numberoftest=len(testans)
ans=clf.predict(testcase)

for counter in range(0,numberoftest):
	#print ans[counter],testans[counter]
	if(ans[counter]==testans[counter]):
		count=count+1
acc=(count*100.0)/numberoftest
print acc




