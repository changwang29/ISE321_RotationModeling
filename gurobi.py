import gurobipy as gp
from gurobipy import GRB

# Create a new model
m = gp.Model("linear")

# Create variables
x = m.addVar(name="x")
y = m.addVar(name="y")

# Set objective: maximize x
m.setObjective(5.0*x + 7.0*y, GRB.MAXIMIZE)

# Add linear constraint: x  <= 6

m.addConstr(x  <= 6, "c1")

# Add bilinear inequality constraint: 3x + 4y <= 24
m.addConstr(3*x + 4*y <= 24, "c2")

# Add bilinear equality constraint: x * z + y * z == 7
m.addConstr(x+ y <= 7, "c3")

# First optimize() call will fail - need to set NonConvex to 2
try:
    m.optimize()
except gp.GurobiError:
    print("Optimize failed due to non-convexity")

# Solve bilinear model
m.Params.NonConvex = 2
m.optimize()

a = m.getObjective()
print(a.getValue())

# m.printAttr('x')

# # Constrain 'x' to be integral and solve again
# x.VType = GRB.INTEGER
# m.optimize()

# m.printAttr('x')
