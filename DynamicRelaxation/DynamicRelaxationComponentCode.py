import Rhino # this is all the Rhino common classes and stuff (documentation here: http://4.rhino3d.com/5/rhinocommon/)
import rhinoscriptsyntax as rs

import sys

import DynamicRelaxation
from DynamicRelaxationPreSpecMaterials import Materials

import itertools
import System.Guid

import clr
clr.AddReference("Grasshopper")
from Grasshopper.Kernel.Data import GH_Path
from Grasshopper import DataTree


"""This component takes as input different sets of lines and points to define a dynamic relaxation (DR) process to find their equilibrium position.

Several things need to be done:
   
    TODO add load elements as triple [position, direction, value]

The code is inspired by the TraerPhysics library for Processing by J. Traer and several amendments/improvements 
made by Guillaume Labelle and Julien Nembrini in TraerAnar as a link to the ANAR+ library (http://anar.ch) 

This code is copyrighted by Julien Nembrini and distributed open source in the sense of the Gnu GPL v3.0. 

"""

#@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
#@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
#@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
#@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@

def makePtFromRhino(pt): 
    return DynamicRelaxation.Point3D(pt.X,pt.Y,pt.Z)
    
def makePtsFromRhino(pts):
    a = []
    for pt in pts:
        a.append(makePtFromRhino(pt))
    return a
    
def makeVecfromPoint3D(p):
    return Rhino.Geometry.Point3d(p.x(),p.y(),p.z())

#@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
#@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
#@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
#@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@

class CurveConstraint(object):
    def __init__(self,crv):
        self.curve = crv
        
    def setCrv(self, crv):
        self.curve = crv
        
    def apply(self,v):
        b,val = Rhino.Geometry.Curve.ClosestPoint(self.curve,makeVecfromPoint3D(v.position))
        if b:
            return makePtFromRhino(self.curve.PointAt(val))
        else :
            v.position

#adjustments
def resetCrv(crvs):
    pass

def resetLoad():
    for i in range(len(allLoads)):
        dir = loads.Branch(i)[0]
        force = loads.Branch(i)[1]
        for j in itertools.islice(allLoads[i],2,None):
            j.setForce(force.X)
            j.setDirection(makePtFromRhino(dir))

def resetMaterials():
    matName = []
    matEval = []
    matAval = []
    matIval = []
    matCval = []
    matDval = []

    for i in range(materials.BranchCount):
        matName.append (materials.Branch(i)[0])
        matEval.append (materials.Branch(i)[1])
        matAval.append (materials.Branch(i)[2])
        matIval.append (materials.Branch(i)[3])
        matCval.append (materials.Branch(i)[4])
        matDval.append (materials.Branch(i)[5])

    #### apply material adjustments to elements

    for bending in allBendings:
        for bend in bending:
            matSpec = bend.getMaterialName()
            bend.setEI( matEval[matName.index(matSpec)], matIval[matName.index(matSpec)] )
            bend.setES( matEval[matName.index(matSpec)], matAval[matName.index(matSpec)] )


#@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
#@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
#@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
#@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@

print 'A prototype for dynamic relaxation in Rhino/GH/python. (c) Julien Nembrini and Paul Nicholas'

#print sys.path

#@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
#@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
#@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
#@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@

# Initialisation
if reset :

    # create particle system no drag no gravity
    ps = DynamicRelaxation.ParticleSystem()
    #ps = ParticleSystem(Vector3D(0,0,1), 0.5)
    #ps.setIntegrator(DynamicRelaxation.ParticleSystem.EULER)

    print ps

    #### materials
    matName = []
    matEval = []
    matAval = []
    matIval = []
    matCval = []
    matDval = []

    for i in range(materials.BranchCount):
        matName.append (materials.Branch(i)[0])
        matEval.append (materials.Branch(i)[1])
        matAval.append (materials.Branch(i)[2])
        matIval.append (materials.Branch(i)[3])
        matCval.append (materials.Branch(i)[4])
        matDval.append (materials.Branch(i)[5])
        
    #### bending elements
    allBendings = [] 
    allBendingsParts = [] 
    for i in range(beams.BranchCount):
        matSpec = beams.Branch(i)[0]
        if type (matSpec) == str:
            for j in itertools.islice(beams.Branch(i),1,None):
                if type(j) is System.Guid:
                    pts = rs.PolylineVertices(j)
                    if pts: 
                        #create the bending elements (registered automagically in ps)
                        parts,bends = DynamicRelaxation.makeBendingsFromList(ps, makePtsFromRhino(pts),matEval[matName.index(matSpec)],matIval[matName.index(matSpec)],matAval[matName.index(matSpec)], matDval[matName.index(matSpec)])
                        for bend in bends:
                            bend.setMaterialName(matSpec)
                        # keep a copy for display of the particles making a bending line
                        allBendingsParts.append(parts)
                        allBendings.append(bends)
        else: print 'problem with beam material definitions'
    print 'bendings :' + str(len(ps.bendings))

    #### elastic elements
    allElastics = [] 
    allElasticsParts = [] 
    
    for i in range(trusses.BranchCount):
        matSpec = trusses.Branch(i)[0]
        if type (matSpec) == str:
            for j in itertools.islice(trusses.Branch(i),1,None):
                if type(j) is System.Guid:
                    pts = rs.PolylineVertices(j)
                    if pts: 
                        #create the bending elements (registered automagically in ps)
                        parts,elas = DynamicRelaxation.makeElasticsFromList(ps, makePtsFromRhino(pts), matEval[matName.index(matSpec)], matAval[matName.index(matSpec)], 0,  matCval[matName.index(matSpec)])
                        # keep a copy for display of the particles making a bending line
                        allElasticsParts.append(parts)
                        allElastics.append(elas)
        else: print 'problem with truss material definitions'
    print 'trusses :' + str(len(ps.elastics))

    #### cables elements
    allCables = [] 
    allCablesParts = [] 

    for i in range(cables.BranchCount):
        matSpec = cables.Branch(i)[0]
        if type (matSpec) == str:
            for j in itertools.islice(cables.Branch(i),1,None):
                if type(j) is System.Guid:
                    pts = rs.PolylineVertices(j)
                    if pts: 
                        parts,cabls = DynamicRelaxation.makeCablesFromList(ps, makePtsFromRhino(pts), matEval[matName.index(matSpec)], matAval[matName.index(matSpec)], 0,  matCval[matName.index(matSpec)])
                        allCablesParts.append(parts)
                        allCables.append(cabls)
        else: print 'problem with cable material definitions'
    print 'cables :' + str(len(ps.cables))
    
    #### loads
    allLoads = [] 
    allLoadsParts = [] 

    for i in range(loads.BranchCount):
        dir = loads.Branch(i)[0]
        force = loads.Branch(i)[1]
        pts = []
        for j in itertools.islice(loads.Branch(i),2,None):
            if j is not None: 
                pts.append (j)
        parts,lds = DynamicRelaxation.makeLoadsFromList(ps, makePtsFromRhino(pts),makePtFromRhino(dir),force.X)
        allLoadsParts.append(parts)
        allLoads.append(lds)
        
    print 'loads :' + str(len(ps.loads))
    
    # TODO make a construction loop for the remaining kind of elements
    #DynamicRelaxation.makeAttractionsFromList(ps, makePtsFromRhino(pts),100)
    
    cPoints = []
    #for pt in pinnedPoints:
    #    if pt is not None: cPoints.append (pt)
    #if len(cPoints)>0:
    #    DynamicRelaxation.makeConstraintsFromList(ps,makePtsFromRhino(cPoints))
    
    # pin constrained points
    for pt in pinnedPoints:
        if pt is not None:
            ps.findParticleEqualToPoint(makePtFromRhino(pt)).makeFixed()
    print 'particles :' + str(len(ps.particles))

    #### line constrained points
    allLineConstraints = []
    for i in range(lineConstrainedPoints.BranchCount):
        if len(lineConstrainedPoints.Branch(i))>1 and lineConstrainedPoints.Branch(i)[0] is not None:
            vect = lineConstrainedPoints.Branch(i)[0]
            pts = []
            for j in itertools.islice(lineConstrainedPoints.Branch(i),1,None):
                if j is not None: 
                    pts.append (j)
            parts = DynamicRelaxation.makeForceConstraintsFromList(ps,makePtsFromRhino(pts),makePtFromRhino(vect), False)
            allRailConstraints.append(parts)
    
    #### rail constrained points
    allRailConstraints = [] 
    for i in range(railConstrainedPoints.BranchCount):
        if len(railConstrainedPoints.Branch(i))>1 and railConstrainedPoints.Branch(i)[1] is not None:
            rail = CurveConstraint(rs.coercecurve(railConstrainedPoints.Branch(i)[0]))
            pts = []
            for j in itertools.islice(railConstrainedPoints.Branch(i),1,None):
                if j is not None: 
                    pts.append (rs.coerce3dpoint(j))
            parts, springs = DynamicRelaxation.makePositionSpringConstraintsFromList(ps, makePtsFromRhino(pts),rail.apply, 1000, 0)
            allRailConstraints.append(parts)

    #### plane constrained points
    allPlaneConstraintPoints = [] 
    for i in range(planeConstrainedPoints.BranchCount):
        if len(planeConstrainedPoints.Branch(i))>1:
            plVect = makePtFromRhino(planeConstrainedPoints.Branch(i)[0])
            pts = []
            for j in itertools.islice(planeConstrainedPoints.Branch(i),1,None):
                if j is not None: 
                    pts.append (j)
            parts = DynamicRelaxation.makeForceConstraintsFromList(ps,makePtsFromRhino(pts),plVect)
            allPlaneConstraintPoints.append(parts)

    stepCount = 0

#@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
#@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@


#check for initialization
initialized = 'stepCount' in locals() or 'stepCount' in globals()
    
#@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
#@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
#@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
#@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@

#adjustment of material parameters during simulation

if adjust:
    if initialized:
        resetMaterials()
        resetLoad()
        #### TODO import other parameters

#@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
#@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
#@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
#@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@

# Dynamic Relaxation step

if run:
    for i in range(10):
        ps.step(step)
    ps.stepRelax(step)
    stepCount += 1
    #print stepCount


#@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
#@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
#@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
#@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@

# Display functions

#center = Rhino.Geometry.Point3d((supportPtsIn[0].X + supportPtsIn[1].X) * .5, (supportPtsIn[0].Y + supportPtsIn[1].Y) * .5, (supportPtsIn[0].Z + supportPtsIn[1].Z) * .5)

if initialized:

    beamsOUT = DataTree[Rhino.Geometry.PolylineCurve]()
    trussesOUT = DataTree[Rhino.Geometry.PolylineCurve]()
    cablesOUT = DataTree[Rhino.Geometry.PolylineCurve]()
    stressOUT = DataTree[float]()
    stressSort = []
    stressMinMax = []
    loadsOUT = DataTree[Rhino.Geometry.Point3d]()
    loadsDirOUT = DataTree[Rhino.Geometry.Vector3d]()
    # compare bending force between top and bottom of arch 
    for i in range(len(allBendings)):
        path = GH_Path(i)
        for j in range(0, len(allBendings[i])+1):
            if j == 0:
                tmpStress = allBendings[i][j].getStress()
            elif j == len(allBendings[i]):
                tmpStress = allBendings[i][j-1].getStress()
            else:
                tmpStress = (allBendings[i][j].getStress()+allBendings[i][j-1].getStress())*0.5
            stressOUT.Add(tmpStress, path)
            stressSort.append(tmpStress)

    if len(stressSort)>0:
        stressSort.sort()
        stressMinMax.append(stressSort[0])
        stressMinMax.append(stressSort[-1])

    for i in range(len(allBendingsParts)):
        path = GH_Path(i)
        parts = []
        for p in allBendingsParts[i] :
            part = Rhino.Geometry.Point3d(p.position.x(), p.position.y(), p.position.z())
            parts.append(part)
        beamsOUT.Add(Rhino.Geometry.PolylineCurve(parts), path)

    for i in range(len(allElasticsParts)):
        path = GH_Path(i)
        parts = []
        for p in allElasticsParts[i] :
            part = Rhino.Geometry.Point3d(p.position.x(), p.position.y(), p.position.z())
            parts.append(part)
        trussesOUT.Add(Rhino.Geometry.PolylineCurve(parts), path)

    for i in range(len(allCablesParts)):
        path = GH_Path(i)
        parts = []
        for p in allCablesParts[i]:
            part = Rhino.Geometry.Point3d(p.position.x(), p.position.y(), p.position.z())
            parts.append(part)
        cablesOUT.Add(Rhino.Geometry.PolylineCurve(parts), path)

    particles = []
    for p in ps.particles:
        part = Rhino.Geometry.Point3d(p.position.x(), p.position.y(), p.position.z())
        particles.append(part)

    for i in range(len(allLoads)):
        path = GH_Path(i)
        parts = []
        for l in allLoads[i]: 
            p = l.getParticle()
            loadsOUT.Add(Rhino.Geometry.Point3d(p.position.x(), p.position.y(), p.position.z()), path)
            loadsDirOUT.Add(Rhino.Geometry.Vector3d(makeVecfromPoint3D(l.getDirection())), path)
    #curveOut = Rhino.Geometry.PolylineCurve(pts)

    stepCounter = stepCount

