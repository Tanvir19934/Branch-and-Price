import gurobipy as gp
from gurobipy import GRB
from typing import List


class SubProblem:

    def __init__(self, d, W, dual_vars, subproblem_model=None):

        self.d = d
        self.W = W
        self.dual_vars = dual_vars
        self.subproblem_model = subproblem_model

    def build_and_optimize_model(self, verbose=True):

        if self.subproblem_model==None:
            self.subproblem_model = gp.Model()
        if verbose == True:
            self.subproblem_model.setParam('OutputFlag', 0)
        self.y = self.subproblem_model.addVars((i for i in range(len(self.dual_vars))), vtype=GRB.INTEGER, lb = 0, ub = GRB.INFINITY, name="y")
        self.subproblem_model.addConstr(gp.quicksum(self.d[i][1] * self.y[i] for i in range(len(self.d)))<= self.W, name = "capacity_constraint")
        self.subproblem_model.setObjective(1-gp.quicksum(self.dual_vars[i] * self.y[i] for i in range(len(self.d))), GRB.MINIMIZE)
        self.subproblem_model.update()
        self.subproblem_model.write("/Users/tanvirkaisar/Library/CloudStorage/OneDrive-UniversityofSouthernCalifornia/Python Projects/Branch and Price/BnP_subproblem.lp")
        self.subproblem_model.optimize()

    def getSolution(self) -> List[int]:
        return self.subproblem_model.getAttr("X")
    
    def cost(self) -> int:
        obj = self.subproblem_model.getObjective()
        return obj.getValue()

class MasterProblem:

    def __init__(self, model):
        self.model = model

    def relaxedLP(self, verbose=True):
        if verbose==True:
            self.model.setParam('OutputFlag', 0)
        else: self.model.setParam('OutputFlag', 1)
        self.model = self.model.relax() #Create the relaxation of a MIP model. Transforms integer variables into continuous variables, and removes SOS and general constraints.
        self.model.optimize()

    def getDuals(self) -> List[int]:
        Pi = []
        for constr in self.model.getConstrs():
            if ('demand' in constr.ConstrName):
                Pi.append(constr.Pi)
        return Pi

    def get_RMP_solution(self) -> List[int]:
        return self.model.getAttr("X")

    def get_RMP_cost(self) -> int:
        obj = self.model.getObjective()
        return obj.getValue()
    
    def addColumn(self, new_column):
        new_column = gp.Column(new_column, self.model.getConstrs())
        self.model.addVar(vtype=GRB.INTEGER, lb = 0, ub = GRB.INFINITY, column=new_column, obj=1) #add the coefficients in the constraint set and the objective function
        self.model.update()
        self.model.write("/Users/tanvirkaisar/Library/CloudStorage/OneDrive-UniversityofSouthernCalifornia/Python Projects/Branch and Price/BnP.lp")