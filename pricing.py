from models import SubProblem, MasterProblem
from initial_RMP import model, d, W
import copy

def column_generation(model, d, W):

    #First, we solve the initial relaxed master problem.
    tol = 1e-4
    master_prob = MasterProblem(model)
    master_prob.relaxedLP(verbose=True)             ## Create the relaxation of a MIP model and optimize it
    if master_prob.model.status==3:
        return None, None, None, None, 3
    obj_val = master_prob.get_RMP_cost()
    RMP_solution = master_prob.get_RMP_solution()
    dual_vars = master_prob.getDuals()

    while True:
        sub_problem = SubProblem(d, W, dual_vars)
        sub_problem.build_and_optimize_model(verbose=True)
        if sub_problem.subproblem_model.status==3:
            return None, None, None, None, 3 
        sub_problem_solution = sub_problem.getSolution()
        sub_problem_cost = sub_problem.cost()
        if sub_problem_cost < 0 - tol:
            new_column = copy.deepcopy(sub_problem_solution)
            #new_column = [0,1,0,1,0]
            master_prob.addColumn(new_column)
            master_prob.relaxedLP(verbose=True)
            if master_prob.model.status==3:
                return None, None, None, None, 3
            dual_vars = master_prob.getDuals()
            obj_val = master_prob.get_RMP_cost()
            RMP_solution = master_prob.get_RMP_solution()
            #print(get_RMP_solution,dual_vars)
        else: break

    is_int = all(isinstance(n, int) or (isinstance(n, float) and n.is_integer()) for n in RMP_solution)
    if RMP_solution:
        status = 1

    return master_prob, RMP_solution, obj_val, is_int, status

def main():
    column_generation(model, d, W)

if __name__ == "__main__":
    main()