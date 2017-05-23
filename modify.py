fopen=open("train.dat","r")
fopen2=open("train2.dat","w")

fopen3=open("test.dat","r")
fopen4=open("test2.dat","w")

fopen5=open("valid.dat","r")
fopen6=open("valid2.dat","w")

numlines=0
for line in fopen:
	if(numlines>10000):
		break
	numlines=numlines+1
	fopen2.write(line)

numlines=0
for line in fopen3:
	if(numlines>10000):
		break
	numlines=numlines+1
	fopen4.write(line)

numlines=0
for line in fopen5:
	if(numlines>10000):
		break
	numlines=numlines+1
	fopen6.write(line)