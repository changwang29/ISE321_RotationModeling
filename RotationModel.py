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

    dict['priority'] =  [("Resident2", "Rotation1", "2")]   
    dict['preference'] = [("Resident1", "Rotation2", "1")]
    dict['impossibleAssignments'] = [("Resident3", "Rotation1", "1")]
    dict['vacation'] = [("Resident1", "1"),("Resident1", "4"),("Resident2", "3")]

    # Parameters
    # Defines parameter for the minimum number of people for each rotation
    p_min = {"Rotation1": 1, "Rotation2": 1, "Rotation3": 1, "Rotation4": 0}

    # Defines parameter for the minimum number of people for each rotation
    p_max = {"Rotation1": 1, "Rotation2": 1, "Rotation3": 2, "Rotation4": 2}

    model(dict)

def getData(i,dict,li):
    df = pd.read_excel("data_rotation.xlsx",usecols=[i])
    df_li = df.values.tolist()
    result = []
    for cell in df_li:
        result.append(cell[0])
    new_result = [item for item in result if not(pd.isnull(item))]
    dict[li[i]] = new_result
    

def model(dict):
    m = gp.Model("rotation_scheduling")
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

if __name__ == "__main__":
    main()
