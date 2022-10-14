# Import Packages
import sys
from operator import truediv
import gurobipy as gp
from gurobipy import GRB
import pandas as pd
import numpy as np
from numpy import nan



def main():
    # Get Data from excel 
    df = pd.read_excel("data_rotation.xlsx")

    # Get list name 
    li =[]
    for j in range(0,6):
        li.append(list(df)[j])

    # Get lists for each sets 
    dict = {}
    i = 0
    for i in range(0,6):
        getData(i,dict,li)

    dict['priority'] =  [("Resident2", "Rotation1", "Block2")]   
    dict['preference'] = [("Resident1", "Rotation2", "Block1")]
    dict['impossibleAssignments'] = [("Resident3", "Rotation1", "Block1")]
    dict['vacation'] = [("Resident1", "Block1"),("Resident1", "Block4"),("Resident2", "Block3")]
    print(dict)
    # Parameters
    # Defines parameter for the minimum number of people for each rotation
    p_min = {"Rotation1": 1, "Rotation2": 1, "Rotation3": 1, "Rotation4": 0}

    # Defines parameter for the minimum number of people for each rotation
    p_max = {"Rotation1": 1, "Rotation2": 1, "Rotation3": 2, "Rotation4": 2}

    # Model 
    m = gp.Model("rotation_scheduling")
    model(m,dict,p_min, p_max)
    solve(m)

def getData(i,dict,li):
    df = pd.read_excel("data_rotation.xlsx",usecols=[i])
    df_li = df.values.tolist()
    result = []
    for cell in df_li:
        result.append(cell[0])
    new_result = [item for item in result if not(pd.isnull(item))]
    dict[li[i]] = new_result
    

def model(m, dict,p_min, p_max):
    
    # Decision Variables 
    # Defines the decision variables (x[p,r,b]=1 if person p assigned to rotation r in block b; x[p,r,b]=0 otherwise)
    x = m.addVars(dict['people'], dict['rotations'], dict['blocks'], vtype=GRB.BINARY, name = "x")

    # Defines variables for consecutive busy rotations
    y = m.addVars(dict['people'], dict['busyRotations'], dict['busyRotations'], dict['blocks'], vtype=GRB.BINARY, name = "y")

    #############
    # OBJECTIVE #
    #############

    m.setObjective(
        sum(1 - y[(p,r1,r2,b)] for p in dict['people'] for r1 in dict['busyRotations'] for r2 in dict['busyRotations'] for b in dict['blocks']) - sum(x[(p, r, b)] for (p,r,b) in dict['preference']), sense = GRB.MINIMIZE
    )
    ###############
    # CONSTRAINTS #
    ###############

    # Ensures one person cannot be assigned two blocks at once
    m.addConstrs((sum(x[(p,r,b)] for r in dict['rotations']) == 1  for p in dict['people'] for b in dict['blocks']),name = "personOneAssignmentPerBlock")

    # Ensures sufficient coverage for each rotation
    m.addConstrs((p_min[r]  <= sum([x[(p,r,b)] for p in dict['people']]) for r in dict['rotations'] for b in dict['blocks']), name = "rotationCoverage_Min" )
    m.addConstrs((p_max[r]  >= sum([x[(p,r,b)] for p in dict['people']]) for r in dict['rotations'] for b in dict['blocks']), name = "rotationCoverage_Max" )

    # Ensures that all-year residents must do each must-do rotation
    m.addConstrs((sum(x[(p,r,b)] for b in dict['blocks']) >= 1  for p in dict['allYearResidents'] for r in dict['mustDo']), name = "AllYear_mustdo")

    # Ensures Priority Assignments are fulfilled
    m.addConstrs((x[(p,r,b)] == 1 for (p,r,b) in dict['priority']), name = "priority")  

    # Ensures rotations that cannot happen, do not happen
    m.addConstrs((x[(p,r,b)] == 0 for (p,r,b) in dict['impossibleAssignments']), name = "impossibleAssignment")

    # Vacations and Interviews constraint that prohibits resident from doing a busy rotation during the vacation or interview period
    m.addConstrs((x[(p,r,b)] == 0 for r in dict['busyRotations'] for (p,b) in dict['vacation']), name = "vacation")

    # Defines y
    m.addConstrs((y[(p,r1,r2,b1)] <= (2 - x[(p,r1,b1)] - x[(p,r2,b2)]) for p in dict['people'] for r1 in dict['busyRotations'] for r2 in dict['busyRotations'] for b1,b2 in zip(dict['blocks'], dict['blocks'][1:])), name = "consecutiveBusyRotation")

def solve(m):
    m.optimize()
    a = m.getObjective()
    print(a.getValue())
    for v in m.getVars():
        if v.x == 1: # When assign the resident to this rotation in the block 
            # print('%s %g' % (v.varName,v.x))
            print(v.varName)

if __name__ == "__main__":
    main()
