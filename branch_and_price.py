from gurobipy import GRB
import heapq
from typing import Dict
import math
from gurobipy import GRB
from initial_RMP import model, d, W
import heapq
from pricing import column_generation

class Node:
    
    def __init__(self, model, depth, name):
        self.model = model
        self.depth = depth
        self.solution = None
        self.obj_val = None
        self.name = name
        print("depth =",self.depth)  #sanity check

    def __lt__(self, other):
        return self.obj_val > other.obj_val  # For heap implementation. The heapq.heapify() will heapify the list based on this criteria.
        
def branching(model):

    # Create the root node by solving the initial rmp
    root_node = Node(model, 0, "root_node")
    master_prob, RMP_solution, obj_val, is_int, status = column_generation(model, d, W)
    if master_prob==None:
        print("Problem infeasible")
        return
    
    #initialize best node and the stack
    best_node = None
    best_obj = GRB.INFINITY
    stack = [root_node]
    heapq.heapify(stack)  #we are going to traverse in best first manner
    
    #loop through the stack
    while stack:
        node = heapq.heappop(stack)
        node.obj_val = obj_val
        node.model = master_prob.model
        if is_int==True:
            if node.obj_val < best_obj:
                best_obj = node.obj_val
                best_node = node
            continue
        else:  
            if node.obj_val > best_obj:
                continue
            else:
                model_vars ={var.VarName: var.X for var in node.model.getVars()}
                var_names = list(model_vars.keys())
                fractional_var = None
                for var in var_names:
                    val = node.model.getVarByName(var).x
                    if val != int(val):
                        fractional_var = var #extract the first fractional variable among the binary variables
                        break

                # Create left branch node
                left_node = Node(node.model.copy(), node.depth + 1, f'{fractional_var}={math.floor(val)}')
                for var in left_node.model.getVars():
                    if var.VarName == fractional_var:
                        var.LB = math.floor(val)
                        var.UB = math.floor(val)
                        left_node.model.update()
                master_prob, RMP_solution, obj_val, is_int, status = column_generation(left_node.model, d, W)
                if status!=3:
                    left_node.obj_val = obj_val
                    left_node.model = master_prob.model
                    heapq.heappush(stack, left_node)

                # Create right branch nodes
                right_node = Node(node.model.copy(), node.depth + 1, f'{fractional_var}={math.ceil(val)}')
                for var in right_node.model.getVars():
                    if var.VarName == fractional_var:
                        var.LB = math.ceil(val)
                        var.UB = math.ceil(val)
                        right_node.model.update()
                master_prob, RMP_solution, obj_val, is_int, status = column_generation(right_node.model, d, W)
                if status!=3:
                    right_node.obj_val = obj_val
                    right_node.model = master_prob.model
                    heapq.heappush(stack, right_node)

    if best_node:
        print("Optimal solution found:")
        model_vars ={var.VarName: var.X for var in best_node.model.getVars()}
        var_names = list(model_vars.keys())
        sol = []
        for var in var_names:
            print(f"{var}: {best_node.model.getVarByName(var).x}")
            sol.append(best_node.model.getVarByName(var).x)
        print(f"Objective value: {best_node.obj_val}")
        constraint_coeffs = retrieve_patterns(best_node.model)
        for item in constraint_coeffs:
            print(constraint_coeffs[item])
    else:
        print("No optimal solution found.")
    
def retrieve_patterns(model) -> Dict:
    '''This function just returns the solution pattern for the cutting stock'''
    constraint_coeffs = {}
    for constr in model.getConstrs():
        coeffs = {}
        for var in model.getVars():
            coeff = model.getCoeff(constr, var)
            if 1:  # Only include non-zero coefficients
                coeffs[var.VarName] = coeff
        constraint_coeffs[constr.ConstrName] = coeffs
    return constraint_coeffs

def main():
    branching(model) #here model is the initial rmp obtained by a simple heuristic from initial_rmp.py

if __name__ == "__main__":
    main()