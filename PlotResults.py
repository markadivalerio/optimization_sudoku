from matplotlib import pyplot as plt 
import pandas as pd
import numpy as np
import math

##################################
# Clues vs Solutions (average)
##################################
results = '../TestingResults.txt'
r = pd.read_csv(results, delimiter=' ')

avgs = pd.DataFrame(r['solutions'].groupby([r['clues']]).mean())
avgs.reset_index(level=0, inplace=True)
logAvgSolutions = np.log(avgs['solutions']) / np.log(10)
avgs['LogAvgSolutions'] = logAvgSolutions

#scatter plot
sp = plt.figure(figsize=(8,8))
sp = plt.scatter(avgs.clues, avgs.solutions, marker = '.')
sp = plt.title("Clues vs. Solutions - 10,000 runs")
sp = plt.xlabel('Clues')
sp = plt.ylabel('Solutions')

sp = plt.show()

#scatter plot log
sp = plt.figure(figsize=(8,8))
sp = plt.scatter(avgs.clues, avgs.LogAvgSolutions, marker = '.')
sp = plt.title("Clues vs. Solutions - 10,000 runs (Log)")
sp = plt.xlabel('Clues')
sp = plt.ylabel('Solutions (Log)')
sp = plt.show()


##################################
# Runs to First Multiple Solutions 
##################################
results = '../TestingMinCluesOneSolution1000Tries.txt'
r = pd.read_csv(results, delimiter=' ')

#scatter plot
sp = plt.figure(figsize=(8,8))
sp = plt.scatter(r.clues, r.runs, marker = '.')
sp = plt.title("Runs to 1st Multiple Solution - 1000 runs")
sp = plt.xlabel('Clues')
sp = plt.ylabel('Model Runs')
sp = plt.show()


##################################
# 1000 Runs - Max Solutions
##################################
results = '../TestingMaxSolutionsByClues1000Tries.txt'
r = pd.read_csv(results, delimiter=' ')

#scatter plot
sp = plt.figure(figsize=(8,8))
sp = plt.scatter(r.clues, r.solutions, marker = '.')
sp = plt.title("1000 Runs - Max Solutions")
sp = plt.xlabel('Clues')
sp = plt.ylabel('Max Solutions')
sp = plt.show()




