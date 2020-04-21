
# from https://stackoverflow.com/questions/45471152/how-to-create-a-sudoku-puzzle-in-python

def generate(base, empties, solutions):
	side  = base*base

	printIt = False

	# pattern for a baseline valid solution
	def pattern(r,c): return (base*(r%base)+r//base+c)%side

	# randomize rows, columns and numbers (of valid base pattern)
	from random import sample
	def shuffle(s): return sample(s,len(s)) 
	rBase = range(base) 
	rows  = [ g*base + r for g in shuffle(rBase) for r in shuffle(rBase) ] 
	cols  = [ g*base + c for g in shuffle(rBase) for c in shuffle(rBase) ]
	nums  = shuffle(range(1,base*base+1))

	# produce board using randomized baseline pattern
	board = [ [nums[pattern(r,c)] for c in cols] for r in rows ]

	if printIt == True:
		print ('\nOriginal:')
		for line in board: print(line)

	squares = side*side
	#empties = squares * 2//4
	#empties = squares - 16
	for p in sample(range(squares),empties):
		board[p//side][p%side] = 0

	if printIt == True:
		print ('\n\nPuzzle Form:')
		numSize = len(str(side))
		for line in board: print("["+"  ".join(f"{n or '.':{numSize}}" for n in line)+"]")



	# put puzzle into form for gurobi 
	# straight text per line with periods for empties 
	# ex: ['.284763..', '...839.2.', '7..512.8.', '..179..4.', '3........', '..9...1..', '.5..8....', '..692...5', '..2645..8']
	row = ''
	listOfRows = []
	for line in board:
		row = ''
		for i in line:
			if i == 0:
				row = row + '.'
			else:
				row = row + str(i)
			#print(i)
		#print (row)
		listOfRows.append(row)

	if printIt == True:
		print('\nGurobi Form:')
		print (listOfRows)	


	rowD = ''
	listOfRowsD = []
	for line in board:
		listOfRowsD.append(line)

	if printIt == True:
		print('\nGurobi Form:')
		print (listOfRowsD)	

	import gurobiSolver as s 

	solutionCount, solutionTime = s.gurobiSolver(listOfRowsD, solutions)

	return solutionCount, solutionTime

