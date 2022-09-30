from operator import truediv
import gurobipy as gp
from gurobipy import GRB

#########
# MODEL #
#########

m = gp.Model("scheduling")

########
# SETS #
########

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

##############
# PARAMETERS #
##############

P = [p for p in people]
R = [r for r in rotations]
B = [b for b in blocks]

# Defines parameter for the minimum number of people for each rotation
p_min = {"Rotation1": 0, "Rotation2": 0, "Rotation3": 0, "Rotation4": 0}

# Defines parameter for the minimum number of people for each rotation
p_max = {"Rotation1": 0, "Rotation2": 0, "Rotation3": 0, "Rotation4": 0}

# Defines parameter for the minimum number of times a person must do the specified rotation
r_min = {[people, rotations]: 0}

# Defines parameter for the maximum number of times a person must do the specified rotation
r_max = {[people, rotations]: 0}

#############
# VARIABLES #
#############

# Defines the decision variables (x[p,r,b]=1 if person p assigned to rotation r in block b; x[p,r,b]=0 otherwise)
x = m.addVars(people, rotations, blocks, vtype=GRB.BINARY)

# Defines variables for consecutive busy rotations
y = m.addVars(people, busyRotations, busyRotations, blocks, vtype=GRB.BINARY)

#############
# OBJECTIVE #
#############

m.setObjective()
class objective:
    def __init__(self, person, rotation, block, allYearResident, partialYearResident, mustDo, busyRotation, priority, preference, impossibleAssignment):
        self.person = person
        self.rotation = rotation
        self.block = block
        self.allYearResident = allYearResident
        self.partialYearResident = partialYearResident
        self.mustDo = mustDo
        self.busyRotation = busyRotation
        self.priority = priority
        self.preference = preference
        self.impossibleAssignment = impossibleAssignment
    


###############
# CONSTRAINTS #
###############

def personOneAssignmentPerBlock(people):
    for p in people:
        for i in range(len(p.rotation)):
            if (p.block[i] + p.rotation > 1):
                return False
    return True

def rotationCoverage(people):
    for p in people:
        for i in range(len(p.rotation)):
            if ( p_max < p.person[i] or p_min > p.person[i]):
                return False
    return True

def peopleRotationBounds(people):
    for p in people:
        for i in range(len(p.rotation)):
            if ( r_max < p.rotation[i] or r_min > p.rotation[i]):
                return False
    return True

def allYearResidentsAssignedToEachMustDoRotation(people):
    for p in people:
        num = 0
        for i in range(len(p.allYearResident)):
            num += p.allYearResident[i]
    if (num >= 1):
        return True
    return False


def priorityAssignments(people):
    for p in people:
        for i in range(len(p.rotation)):
            if ( p.priority[i] == 0):
                return False
    return True

def assignmentsThatCannotHappen(people):
    for p in people:
        for i in range(len(p.rotation)):
            if ( p.impossibleAssignment[i] == 1):
                return False
    return True





#########
# SOLVE #
#########

# NEEDS IMPLEMENTATION

###########
# DISPLAY #
###########

def display(people):
    for p in people:
        for i in range(len(p.rotation)):
            print (p.person[i] + " " + p.rotation[i] + " " + p.block[i])
            


