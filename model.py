# Useful Links:
# https://www.youtube.com/watch?v=vnLc_3VnVcw
# https://www.youtube.com/watch?v=0EUX3ua2liU
import gurobipy as gp
from gurobipy import GRB

# Model
m = gp.Model("scheduling")

# Sets & Parameters
# Defines the (ordered) set of people
people = ["Resident1", "Resident2", "Resident3", "Resident4"]

# Defines the (ordered) set of rotations
rotations = ["Rotation1", "Rotation2", "Rotation3", "Rotation4"]

# Defines the (ordered) set of blocks
blocks = ["1", "2", "3", "4"]

# Defines the set of residents who are around for the entire year
allYearResidents = {"Resident1": 1, "Resident2": 1, "Resident3": 1, "Resident4": 0}

# Defines the set of residents who are around for a partial year
partialYearResidents = {"Resident1": 0, "Resident2": 0, "Resident3": 0, "Resident4": 1}

# Defines the rotations that all-year residents must do
mustDo = {"Rotation1": 1, "Rotation2": 1, "Rotation3": 1, "Rotation4": 0}

# Defines the rotations that are nonessential
# NOT INCLUDED #

# Defines parameter indicating busy rotations
busyRotations = {"Rotation1": 1, "Rotation2": 1, "Rotation3": 0, "Rotation4": 0}

# Defines the rotations during which vacations are allowed
# NOT INCLUDED #

# Defines set of priority assignments
priority = {"priority1": {"Resident2": 1, "Rotation1": 1, "2": 1}} # Not sure if it is correct implementation


# Defines set of preference assignments
preference = {"preference1": {"Resident1": 1, "Rotation2": 1, "1": 1}} # Not sure if it is correct implementation

# Defines set of impossible assignments
impossibleAssignments = {"impossible1": {"Resident3": 1, "Rotation1": 1, "1": 1}}

# Defines set of blocks in which a person is gone
# NOT INCLUDED #

# Defines set of impossible rotations for people
# NOT INCLUDED #

# Defines set of impossible rotations for blocks
# NOT INCLUDED #

# Defines parameter for the minimum number of people for each rotation
p_min = {rotations: 0} # Not sure if it is correct implementation

# Defines parameter for the minimum number of people for each rotation
p_max = {rotations: 0} # Not sure if it is correct implementation

# Defines parameter for the minimum number of times a person must do the specified rotation
r_min = {people: 0, rotations:0} # Not sure if it is correct implementation

# Defines parameter for the maximum number of times a person must do the specified rotation
r_max = {people: 0, rotations: 0} # Not sure if it is correct implementation

# Variables
# Useful links:
# https://www.gurobi.com/documentation/9.5/refman/py_model_addvars.html
# https://www.gurobi.com/documentation/9.5/refman/variables.html
# Defines the decision variables (x[p,r,b]=1 if person p assigned to rotation r in block b; x[p,r,b]=0 otherwise)
p = m.addVar(vType=GRB.BINARY, name="p")
r = m.addVar(vType=GRB.BINARY, name="r")
b = m.addVar(vType=GRB.BINARY, name="b")

# Defines variables for consecutive busy rotations
