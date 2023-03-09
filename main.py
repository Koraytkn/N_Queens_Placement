import numpy as np
import sys
from contextlib import redirect_stdout

x = 0

def QueensHalfLasVegas(n,k):
	global x
	AvailColumns = []
	AllColumns = []
	for i in range(n):
		AvailColumns.append(i)
		AllColumns.append(i)
	R=0
	Column = []
	while(len(AvailColumns) != 0 and R <= n-1):								#Until some point (R>=k) we can use QueensLaasVegas that we have implemented for part1 
		numOfAvailableC = len(AvailColumns)
		nextColumnI = np.random.randint(0,numOfAvailableC)
		C=AvailColumns[nextColumnI]
		Column.append(C)
		R +=1
		if(R==1 and k==0):
			del Column[0]
			R-=1
			break
		AllListToShrink = []
		for element in AllColumns:
			AllListToShrink.append(element)
		InvalidColumns = []
		for i in range(len(Column)):
			difference = R-i
			possibleOut1 = Column[i] + difference
			possibleOut2 = Column[i] - difference
			if(possibleOut1<= n-1):
				InvalidColumns.append(possibleOut1)
			if(possibleOut2 >=0):
				InvalidColumns.append(possibleOut2)
		for kk in range(len(InvalidColumns)):
			takeOut = InvalidColumns[kk]
			if(takeOut in AllListToShrink):
				AllListToShrink.remove(takeOut)
		for l in range(len(Column)):
			takeOut = Column[l]
			if(takeOut in AllListToShrink):
				AllListToShrink.remove(takeOut)
		AvailColumns = AllListToShrink
		if(R>=k):
			break
	if(R< k ):																#checking if we were able to place k queens as requested
		return False                                     
			
	twoDimensionalBackTrace= []		
	while(R<n):	
		if(len(AvailColumns)==0):
			break
		twoDimensionalBackTrace.append(AvailColumns)	
		pivot = AvailColumns[0]												#selecting the left most available column for first choice at each step for deterministic part 
		
		Column.append(pivot)
		R +=1
		if(R==n):
			x+=1
			return True               
		AllListToShrink = []
		for element in AllColumns:
			AllListToShrink.append(element)
		InvalidColumns = []
		for i in range(len(Column)):
			difference = R-i
			possibleOut1 = Column[i] + difference
			possibleOut2 = Column[i] - difference
			if(possibleOut1<= n-1):
				InvalidColumns.append(possibleOut1)
			if(possibleOut2 >=0):
				InvalidColumns.append(possibleOut2)
		for kk in range(len(InvalidColumns)):
			takeOut = InvalidColumns[kk]
			if(takeOut in AllListToShrink):
				AllListToShrink.remove(takeOut)
		for l in range(len(Column)):
			takeOut = Column[l]
			if(takeOut in AllListToShrink):
				AllListToShrink.remove(takeOut)
		AvailColumns = AllListToShrink	
		if(len(AvailColumns)==0):											#If we have come to a dead end we need to make some checks 
			selection = Column[R-1]
			R -=1
			newAvailable = twoDimensionalBackTrace[R-k]
			newAvailable.remove(selection)									#Taking the last option that has sragged us in to a dead end out of stack 
			del Column[R]
			if(len(newAvailable)==0):
				del twoDimensionalBackTrace[R-k]
				if(len(twoDimensionalBackTrace)==0):						# That return true means don t increment the x (counts for success) but also let the main know k placements were successful
					return True
				else:
					checker = 0
					while(len(twoDimensionalBackTrace)!=0):					# Until there is a choice we have made which can be altered we continue to pop the previous decisions
						lastselected = Column[R-1]
						R -=1
						shrinkedAvailable = twoDimensionalBackTrace[R-k]	
						shrinkedAvailable.remove(lastselected)
						del Column[R]
						del twoDimensionalBackTrace[R-k]
						if(len(shrinkedAvailable)!=0):
							checker = 1
							AvailColumns = shrinkedAvailable
							break
					if(len(twoDimensionalBackTrace)==0  and checker!=1):
						return True
							
			else:
				AvailColumns= newAvailable
				del twoDimensionalBackTrace[R-k]
	return True

def QueensLasVegas(n):
	global x															# xounting the successful trials
	AvailColumns = []
	AllColumns = []
	for i in range(n):
		AvailColumns.append(i)
		AllColumns.append(i)
	R=0
	Column = []
	strforFile=""
	while(len(AvailColumns) != 0 and R <= n-1):									#Implementatiton of pseudocode 
		numOfAvailableC = len(AvailColumns)
		nextColumnI = np.random.randint(0,numOfAvailableC)
		C=AvailColumns[nextColumnI]
		Column.append(C)
		R +=1
		AllListToShrink = []
		for element in AllColumns:
			AllListToShrink.append(element)
		InvalidColumns = []
		for i in range(len(Column)):
			difference = R-i
			possibleOut1 = Column[i] + difference
			possibleOut2 = Column[i] - difference
			if(possibleOut1<= n-1):
				InvalidColumns.append(possibleOut1)
			if(possibleOut2 >=0):
				InvalidColumns.append(possibleOut2)
		for k in range(len(InvalidColumns)):
			takeOut = InvalidColumns[k]
			if(takeOut in AllListToShrink):
				AllListToShrink.remove(takeOut)
		for l in range(len(Column)):
			takeOut = Column[l]
			if(takeOut in AllListToShrink):
				AllListToShrink.remove(takeOut)
		AvailColumns = AllListToShrink
		strforFile += "Step "+str(R)+": Columns: ["									#Creating the string to return and write to outfile at each step
		strT = ", ".join(str(a) for a in Column)
		strforFile+= strT + "]\n"
		strforFile += "Step "+str(R)+": Available: ["
		strTT = ", ".join(str(a) for a in AvailColumns)
		strforFile += strTT + "]\n"

		if(len(Column) == n):
			x += 1
			return "Successful\n" + strforFile
	return "Unsuccessful\n" + strforFile
	
partSelection = sys.argv[1]

if(partSelection=="part1"):															#Taking output as requested for part1
	for i in range(6,12,2):
		x=0
		n=i
		filename = "results_"+str(i)+".txt"
		f = open(filename, "w")
		for aa in range(10000):
			stringEnd = QueensLasVegas(n)
			with redirect_stdout(f):
					print(stringEnd)
		print("LasVegas Algorithm With n =",n)
		print("Number of successful placements is",x)
		print("Number of trials is 10000")
		print("Probability that it will come to a solution is",x/10000, "\n")
elif(partSelection=="part2"):														#Taking output as requested for part2 
	for i in range(6,12,2):
		x=0
		n=i
		print("---------------",n,"---------------")
		for k in range(n):
			print("k is", k)
			x=0
			for aaa in range(10000):
				currentStatus = QueensHalfLasVegas(n,k)		
				while(not currentStatus):
					currentStatus = QueensHalfLasVegas(n,k)
			print("Number of successful placements is",x)
			print("Number of trials is 10000")
			print("Probability that it will come to a solution is",x/10000)
		print()		

