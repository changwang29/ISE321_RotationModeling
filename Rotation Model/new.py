import sys
from operator import truediv
import gurobipy as gp
from gurobipy import GRB
import pandas as pd
import numpy as np
from numpy import nan
import sqlite3
from pandas import read_sql_table, read_sql_query

def main():

    # Connect with Database
    path = '/Users/chang/Desktop/School/Fall2022/ISE321/Rotation Model/data.db'
    con = sqlite3.connect(path)
    con.row_factory = lambda cursor, row: row[0]
    c = con.cursor()
    dict = {}
    p_min, p_max = getData(dict,c)

    # Model 
    m = gp.Model("rotation_scheduling")
    model(m,dict,p_min, p_max)
    solve(m)
    

def getData(dict,c):

    people = c.execute('SELECT name FROM resident WHERE name IS NOT ""').fetchall()
    allYearResidents = c.execute('SELECT name FROM resident Where allYear = "y"').fetchall()
    rotations = c.execute('SELECT Rotation_name FROM rotation WHERE Rotation_name IS NOT ""').fetchall()
    mustDo = c.execute('SELECT Rotation_name FROM rotation Where mustDo = "y"').fetchall()
    busyRotations = c.execute('SELECT Rotation_name FROM rotation Where busy = "y"').fetchall()
    dict['people'] = people
    dict['allYearResidents'] = allYearResidents
    dict['rotations'] = rotations
    dict['mustDo'] = mustDo
    dict['busyRotations'] = busyRotations

    # Inputs that still need to add to interface 
    dict['blocks'] = ["Block1", "Block2", "Block3", "Block4"]
    dict['priority'] =  [("Resident2", "Rotation1", "Block2")]   
    dict['preference'] = [("Resident1", "Rotation2", "Block1")]
    dict['impossibleAssignments'] = [("Resident3", "Rotation1", "Block1")]
    dict['vacation'] = [("Resident1", "Block1"),("Resident1", "Block4"),("Resident2", "Block3")]
    p_min = {"Rotation1": 1, "Rotation2": 1, "Rotation3": 1, "Rotation4": 0}
    p_max = {"Rotation1": 1, "Rotation2": 1, "Rotation3": 2, "Rotation4": 2}
    
    return p_min, p_max

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

    constraints(m,p_min,p_max,dict,x,y)
    
def constraints(m, p_min, p_max, dict,x,y):
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