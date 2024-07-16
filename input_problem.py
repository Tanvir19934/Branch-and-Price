'''Consider a company that has a supply of boards of
of width W. (We assume that W is a positive integer.) However, customr demand is for smaller widths of board; in particular b_i boards of width w_i
i = 1,2, ... ,m, need to be produced. We assume that w_i <= W for each i
and that each w_i is an integer.
The goal of the company is to minimize the number of boards to be cut while satisfying customer demand.

The optimization problem to be solved is:


minimize,   sum_(j=1 to n) x_j
s.t.,       sum_(j=1 to n) a_(i,j) * x_j = b_i  for i = 1,......,m
            x_j >= 0, and integer                for j = 1,......,n

    
where, x_j be the number of boards cut according to pattern j.
a_(i,j) indicates how many boards of width w_i are produced by that pattern.
b_i is the number of boards of width w_i are needed by the customer.

Reference: Introduction to Linear Optimization by Dimitris Bertsimas, chapter 6'''

W = 100  #The width of the available stocks (same for all stocks)
d = [(45, 22), (38, 42), (25, 52),(11, 53), (12, 78)] #This is demand specification, expressed as a tuple: (number of board needed = b_i, width of that needed board = w_i)

