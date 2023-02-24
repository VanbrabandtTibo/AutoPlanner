from pulp import *

# Create a maximization problem
prob = LpProblem("Example problem", LpMaximize)

# LpInteger indicates that the variable must take an integer value
# 1) Define decision variables
x = LpVariable("x", lowBound=0, cat=LpInteger)
y = LpVariable("y", lowBound=0, cat=LpInteger)

# 2) Define objective function
prob += 3*x + 2*y

# 3) Define constraints
prob += x + y <= 4
prob += x - y >= 1
prob += 2*x + y <= 8

# Solve the problem
status = prob.solve()

# Print the solution
print("Status:", LpStatus[status])
print("Objective value:", value(prob.objective))
print("x =", value(x))
print("y =", value(y))