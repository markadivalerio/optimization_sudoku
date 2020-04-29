import numpy as np
import gurobi as gp
from gurobipy import GRB, quicksum, max_, abs_

def create_empty_grid(size=9):
    return np.zeros((size,size))

def load_test():
    grid = create_empty_grid(9)

    grid[0][2]=7
    grid[0][5]=4
    grid[0][8]=1
    grid[1][3]=2
    grid[1][4]=8
    grid[2][0]=2
    grid[2][2]=6
    grid[2][5]=9
    grid[3][1]=5
    grid[3][6]=2
    grid[3][8]=6
    grid[4][1]=1
    grid[4][4]=2
    grid[4][7]=9
    grid[5][0]=6
    grid[5][2]=4
    grid[5][7]=7
    grid[6][3]=8
    grid[6][6]=9
    grid[6][8]=2
    grid[7][4]=7
    grid[7][5]=2
    grid[8][0]=8
    grid[8][3]=4
    grid[8][6]=6

    return grid

def gurobi_solution(grid, binary=True):
    # In the MIP formulation, binary variables x[i,j,v] indicate whether
    # cell <i,j> takes value 'v'.  The constraints are as follows:
    #   1. Each cell must take exactly one value (sum_v x[i,j,v] = 1)
    #   2. Each value is used exactly once per row (sum_i x[i,j,v] = 1)
    #   3. Each value is used exactly once per column (sum_j x[i,j,v] = 1)
    #   4. Each value is used exactly once per 3x3 subgrid (sum_grid x[i,j,v] = 1)

    n = len(grid[0])
    s = int(n ** 0.5)
    model = gp.Model('gurobi')
    model.Params.LogToConsole = 0
    type = GRB.BINARY if binary else GRB.CONTINUOUS
    var = model.addVars(n, n, n, vtype=type, name='G')

    # Fix variables associated with cells whose values are pre-specified
    for i in range(n):
        for j in range(n):
            if grid[i][j] > 0:
                v = int(grid[i][j]) - 1
                var[i, j, v].LB = 1

    # Each cell must take one value
    model.addConstrs((var.sum(r, c, '*') == 1
                      for r in range(n)
                      for c in range(n)), name='V')

    # Each value appears once per row
    model.addConstrs((var.sum(r, '*', v) == 1
                      for r in range(n)
                      for v in range(n)), name='R')

    # Each value appears once per column
    model.addConstrs((var.sum('*', c, v) == 1
                      for c in range(n)
                      for v in range(n)), name='C')

    # Each value appears once per subgrid
    model.addConstrs((
        gp.quicksum(var[i, j, v] for i in range(i0 * s, (i0 + 1) * s)
                    for j in range(j0 * s, (j0 + 1) * s)) == 1
        for v in range(n)
        for i0 in range(s)
        for j0 in range(s)), name='Sub')

    model.optimize()

    return model, var


def print_solution(grid, model, variables):
    print('')
    print('Solution:')
    print('')
    n = len(grid[0])
    s = int(n ** 0.5)

    # Retrieve optimization result

    solution = model.getAttr('X', variables)

    print('Time: %s' % model.RunTime)

    for i in range(n):
        sol = ''
        if i != 0 and i % s == 0:
            sol += '\n'
        for j in range(n):
            if j != 0 and j % s == 0:
                sol += '  '
            for v in range(n):
                sol += str(solution[i, j, v])
                # if solution[i, j, v] > 0.5:
                #     sol += str(v + 1)
        print(sol)


def gurobi_solution2(grid, si, sj, sols=1, binary=True):
    # In the MIP formulation, binary variables x[i,j,v] indicate whether
    # cell <i,j> takes value 'v'.  The constraints are as follows:
    #   1. Each cell must take exactly one value (sum_v x[i,j,v] = 1)
    #   2. Each value is used exactly once per row (sum_i x[i,j,v] = 1)
    #   3. Each value is used exactly once per column (sum_j x[i,j,v] = 1)
    #   4. Each value is used exactly once per 3x3 subgrid (sum_grid x[i,j,v] = 1)

    n = len(grid[0])
    model = gp.Model('gurobi')
    model.Params.LogToConsole = 0
    type = GRB.BINARY if binary else GRB.CONTINUOUS

    if sols > 1:
        model.Params.LogToConsole = 0
        model.params.OutputFlag = 0
        model.Params.PoolSolutions = sols
        model.Params.PoolSearchMode = 2

    var = model.addVars(n, n, n, vtype=type, name='G')

    # Fix variables associated with cells whose values are pre-specified
    for i in range(n):
        for j in range(n):
            if grid[i][j] > 0:
                v = int(grid[i][j]) - 1
                var[i, j, v].LB = 1

    # Each cell must take one value
    model.addConstrs((var.sum(r, c, '*') == 1
                      for r in range(n)
                      for c in range(n)), name='V')

    # Each value appears once per row
    model.addConstrs((var.sum(r, '*', v) == 1
                      for r in range(n)
                      for v in range(n)), name='R')

    # Each value appears once per column
    model.addConstrs((var.sum('*', c, v) == 1
                      for c in range(n)
                      for v in range(n)), name='C')

    # Each value appears once per subgrid
    model.addConstrs((
        gp.quicksum(var[i, j, v] for i in range(i0 * sj, (i0 + 1) * sj)
                    for j in range(j0 * si, (j0 + 1) * si)) == 1
        for v in range(n)
        for i0 in range(si)
        for j0 in range(sj)), name='Sub')

    model.optimize()

    solution = np.zeros((n, n))
    sol = model.getAttr('X', var)
    for i in range(n):
        for j in range(n):
            for v in range(n):
                if sol[i, j, v] > 0.5:
                    solution[i][j] = v + 1

    return model, var, solution, model.SolCount


def print_solution2(grid, model, variables, si, sj):
    print('')
    print('Solution:')
    print('')
    n = len(grid[0])

    # Retrieve optimization result

    solution = model.getAttr('X', variables)

    for i in range(n):
        sol = ''
        if i != 0 and i % sj == 0:
            sol += '\n'
        for j in range(n):
            if j != 0 and j % si == 0:
                sol += '  '
            for v in range(n):
                if solution[i, j, v] > 0.5:
                    sol += str(v + 1).rjust(n // 10 + 2)
        print(sol)

def load_sample():
    grid = load_test()
    model, var = gurobi_solution(grid)
    print_solution(grid, model, var)

def load_all():
    array = np.load(file='all_runs.npy', allow_pickle=True)
    results = array.item()

    for item in results.items():

        name = item[0]
        data = item[1]

        si = data['si']
        sj = data['sj']

        iterations = data['results']

        total_bin_time = 0
        bin_count = 0
        total_lin_time = 0
        lin_count = 0

        for i, iteration in enumerate(iterations):

            grid = iteration['sparsed']
            # shape = "%sx%s" % (grid.shape[0], grid.shape[1])
            clues = iteration['clue_count']

            model = None
            model2 = None

            # If dimensions are equal, use the original solver.
            if si == sj:
                model, var = gurobi_solution(grid)
                # print_solution(grid, model, var)
                # Now, check the solution when we don't use binary variables.
                model2, var2 = gurobi_solution(grid, binary=False)
                # print_solution(grid, model2, var2)

                total_bin_time += model.RunTime
                bin_count += 1

                if model.getAttr('X', var) == model2.getAttr('X', var2):
                    print('Equal    : %s %i: bin %.5f lin %.5f delta %.5f clues %s' % (name, i, model.RunTime, model2.RunTime, model.RunTime - model2.RunTime, clues))
                    total_lin_time += model2.RunTime
                    lin_count += 1
                else:
                    print("Not Equal: %s %i: bin %.5f %s" % (name, i, model.RunTime, clues))

            else:
                model, var, sols, sol_count = gurobi_solution2(grid, si, sj)
                # print_solution2(grid, model, var, si, sj)
                model2, var2, sols2, sol_count2 = gurobi_solution2(grid, si, sj, binary=False)
                # print_solution2(grid, model2, var2, si, sj)

                total_bin_time += model.RunTime
                bin_count += 1

                if model.getAttr('X', var) == model2.getAttr('X', var2):
                    print('Equal    : %s %i: bin %.5f lin %.5f delta %.5f clues %s' % (name, i, model.RunTime, model2.RunTime, model.RunTime - model2.RunTime, clues))
                    total_lin_time += model2.RunTime
                    lin_count += 1
                else:
                    print("Not Equal: %s %i: bin %.5f %s" % (name, i, model.RunTime, clues))



            # print('%s %i: %.5f %.5f %.5f' % (result, i, model.RunTime, model2.RunTime, model.RunTime - model2.RunTime))

        average_bin_time = total_bin_time / bin_count if bin_count > 0 else 0
        average_lin_time = total_lin_time / lin_count if lin_count > 0 else 0

        print("TOTAL: solved %s of %s bin %.5f lin %.5f delta %.5f" % (bin_count, len(iterations), average_bin_time, average_lin_time, average_bin_time - average_lin_time))


# load_sample()
load_all()