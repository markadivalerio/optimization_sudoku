import SudokuGenerator as sg

base = 3
side  = base*base

squares = side*side
empties = squares * 2//4
empties = squares - 10

solutions = 500000

f = open("TestingResults17_500000.txt", "w")

#for j in range(15, squares + 1): # decrease the empties
if 1 == 1:
	j = 17
	empties = squares - j
	#print ('empties: ' + str(j))
	for i in range(1): # n model runs

		solutionCount, solutionTime = sg.generate(base, empties, solutions)
		print (str(i) + ': ' + str(base) + ' ' + str(j) + ' ' + str(solutionCount) + ' ' + str(solutionTime) )
		f.write(str(base) + ' ' + str(j) + ' ' + str(solutionCount) + ' ' + str(solutionTime) + '\n')

f.close()

