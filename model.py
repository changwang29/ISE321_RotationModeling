import gurobipy as gp
from gurobipy import GRB

# Create a new model
m = gp.Model("linear")

# Create variables
x = m.addVar(name="x")
y = m.addVar(name="y")