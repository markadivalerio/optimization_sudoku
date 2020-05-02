import SudokuGenerator as sg

base = 3
side  = base*base

squares = side*side
empties = squares * 2//4
empties = squares - 30

solutions = 10

f = open("TestingMinCluesOneSolution.txt", "w")

if 1 == 2: # 
	for j in range(55, squares + 1): # decrease the empties
		#if 1 == 1:
			#j = 17
		empties = squares - j
		#print ('empties: ' + str(j))
		for i in range(100): # n model runs

			solutionCount, solutionTime = sg.generate(base, empties, solutions)
			#print (str(i) + ': ' + str(base) + ' ' + str(j) + ' ' + str(solutionCount) + ' ' + str(solutionTime) )
			#print ('i: ' + str(i) + ' j: ' + str(j))
			f.write(str(base) + ' ' + str(j) + ' ' + str(solutionCount) + ' ' + str(solutionTime) + '\n')

	f.close()

if 1 == 1:
	f = open("TestingMinCluesOneSolution1000Tries.txt", "w")
	f.write ('runs clues solutions\n')
	# show howm many model runs it took to find more than one solution; 1000 tries
	for j in range(55, 75): # decrease the empties
		#if 1 == 1:
			#j = 17
		empties = squares - j
		#print ('empties: ' + str(j))
		for i in range(1000): # n model runs

			solutionCount, solutionTime = sg.generate(base, empties, solutions)

			if solutionCount > 1:
				#print (str(i) + ': ' + str(base) + ' ' + str(j) + ' ' + str(solutionCount) + ' ' + str(solutionTime) )
				break
			
		print (str(i + 1) + ' ' + str(j) + ' ' + str(solutionCount)  )
		f.write(str(i + 1) + ' ' + str(j) + ' ' + str(solutionCount) + '\n')

	f.close()

exit(0)

f = open("TestingMaxSolutionsByClues1000Tries.txt", "w")
f.write ('base clues solutions\n')
for j in range(55, 75): # decrease the empties
	#if 1 == 1:
		#j = 17
	empties = squares - j
	#print ('empties: ' + str(j))
	maxSolutionCount = 0

	for i in range(1000): # n model runs

		solutionCount, solutionTime = sg.generate(base, empties, solutions)

		if solutionCount > maxSolutionCount:
			#print (str(i) + ': ' + str(base) + ' ' + str(j) + ' ' + str(solutionCount) + ' ' + str(solutionTime) )
			maxSolutionCount =  solutionCount
		
	print (str(i) + ': ' + str(base) + ' ' + str(j) + ' ' + str(maxSolutionCount) )
	f.write(str(base) + ' ' + str(j) + ' ' + str(maxSolutionCount) + '\n')

f.close()
