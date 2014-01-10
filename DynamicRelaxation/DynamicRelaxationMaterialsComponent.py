from DynamicRelaxationPreSpecMaterials import Materials

import clr
clr.AddReference("Grasshopper")
from Grasshopper.Kernel.Data import GH_Path
from Grasshopper import DataTree

PreSpecMatList = userDefined
exLength = PreSpecMatList.BranchCount

mat = Materials()

# I is the second moment of area 
#   http://en.wikipedia.org/wiki/Second_moment_of_area
#   http://en.wikipedia.org/wiki/List_of_area_moments_of_inertia
# A is the section area
# D is the distance to the neutral axis in the the direction in which I is computed

for preset in preSpecified:
    exLength += 1
    if preset == 0:#GFRP_D2
        for i in mat.gfrp(NAME = 'GFRP_D2', A = 3.1415, I = 0.78539, D = 1):
            PreSpecMatList.Add(i, GH_Path(exLength))
    elif preset == 1:#GFRP_D3
        for i in mat.gfrp(NAME = 'GFRP_D3', A = 7.068375, I = 3.976078, D = 1.5):
            PreSpecMatList.Add(i, GH_Path(exLength))
    elif preset ==2:#STEEL_D2
        for i in mat.steel(NAME = 'STEEL_D2', A = 3.1415, I = 0.78539, D = 1):
            PreSpecMatList.Add(i, GH_Path(exLength))
    elif preset ==3:#RATTAN_D6
        for i in mat.rattan(NAME = 'RATTAN_D6', A = 28.2735, I = 63.617251, D = 3):
            PreSpecMatList.Add(i, GH_Path(exLength))
    elif preset ==4:#RATTAN_D10
        for i in mat.rattan(NAME = 'RATTAN_D10', A = 78.5375, I = 490.873852, D = 5):
            PreSpecMatList.Add(i, GH_Path(exLength))
    elif preset ==5:#WOOD_2*20
        for i in mat.wood(NAME = 'WOOD_2x20', A = 40, I = 13.333333, D = 1):
            PreSpecMatList.Add(i, GH_Path(exLength))
    elif preset ==6:#MEMBRANE
        for i in mat.membrane(NAME = 'MEMBRANE', A = 0.01, C = 0.9):
            PreSpecMatList.Add(i, GH_Path(exLength))
    elif preset ==7:#PVC
        for i in mat.pvc(NAME = 'PVC_D2', A = 3.1415, I = 0.78539, D = 1):
            PreSpecMatList.Add(i, GH_Path(exLength))
        
        
        
a = PreSpecMatList