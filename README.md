# Branch-and-Price
This is an implementation of the Branch and Price algorithm for solving large scale integer programs. The sample problem solved in this code is the classic cutting stock problem (Reference: Introduction to Linear Optimization by Dimitris Bertsimas, chapter 6). The purpose of this repository is to provide a step-by-step implementation of the Branch and Price algorithm. However, please note that some steps are highly dependent on the actual problem structure and not every integer programs are suitable for this algorithm.

A flowchart of the Branch and Price algorithm is uploaded in the repository. More details on the algorithm can be found at:
https://grzegorz-siekaniec.github.io/bits-of-this-bits-of-that/2021/solving-generalized-assignment-problem-using-branch-and-price.html#branching-rule

Here is a description of the problem:

Consider a company that has a supply of boards of
of width W. (We assume that W is a positive integer.) However, customr demand is for smaller widths of board; in particular b_i boards of width w_i
i = 1,2, ... ,m, need to be produced. We assume that w_i <= W for each i
and that each w_i is an integer.
The goal of the company is to minimize the number of boards to be cut while satisfying customer demand.

The optimization problem to be solved is:


minimize,   sum_(j=1 to n) x_j
s.t.,       sum_(j=1 to n) a_(i,j) * x_j = b_i   for i = 1,......,m
            x_j >= 0, and integer                for j = 1,......,n

    
where, x_j be the number of boards cut according to pattern j.
a_(i,j) indicates how many boards of width w_i are produced by that pattern.
b_i is the number of boards of width w_i are needed by the customer.
