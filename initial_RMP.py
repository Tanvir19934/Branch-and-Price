import gurobipy as gp
from gurobipy import GRB, quicksum
import math
from input_problem import *
from typing import List, Tuple

def feasible_solution(W:int, d: List[Tuple[int,int]]) -> List[int]:
    sol = []
    for item in d:
        sol.append(math.floor(W/item[1]))
    return sol

feasible_sol = feasible_solution(W,d)

m = len(d)  
M = [i for i in range(m)]
matrix = [[0 for _ in range(m)] for _ in range(m)]

for i in range(m):
    matrix[i][i] = feasible_sol[i]

model = gp.Model()
x = model.addVars((item for item in M), vtype = GRB.INTEGER, lb = 0, ub = GRB.INFINITY, name = "x")

model.addConstrs((quicksum(x[i]*matrix[j][i] for i in range(m)) >= d[j][0] for j in range(m)), name='demand')
model.setObjective(quicksum(x[i] for i in range(m)))

model.update()

model.write("/Users/tanvirkaisar/Library/CloudStorage/OneDrive-UniversityofSouthernCalifornia/Python Projects/Branch and Price/initial_rmp.lp")