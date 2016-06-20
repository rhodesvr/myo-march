"""
 Represents the visual environment the user interacts with.
 Additionally, this contains the objects in the experiments,
 such as cylinders and arrows
===
 Maybe, it should not be tied as much to cylinders and such, but instead an initial view?
"""

class Environment(object):
    view = 0
    # these are the visual objects the user sees
    objectLocations = []
    # these are the positions of the cylinders
    cylinderLocations = []
    # these are the positions of the arrows
    arrowLocations = []
    # objects to face in a given spot
    spotObjects = []
    # order to face objects in a given spot
    objectOrder = []
    # order in which to go to various cylinders
    cylinderOrder = []

    #current object and cylinder maybe?
    def initView(self):
        raise NotImplementedError( "Should have implemented this" )
    def initCylinder(self, cylName):
        raise NotImplementedError( "Should have implemented this" )
    def initArrow(self, arrowName):
        raise NotImplementedError( "Should have implemented this" )
    def initObjectLocations(self):
        raise NotImplementedError( "Should have implemented this" )
    def initCylinderLocation(self):
        raise NotImplementedError( "Should have implemented this" )
    def initArrowLocations(self):
        raise NotImplementedError( "Should have implemented this" )
    def initSpotObjects(self):
        raise NotImplementedError( "Should have implemented this" )
    def initObjectOrder(self):
        raise NotImplementedError( "Should have implemented this" )
    def initCylinderOrder(self):
        raise NotImplementedError( "Should have implemented this" )
    # might take speed/ angle/step object later...
    def movePerson(self, angle):
        raise NotImplementedError( "Should have implemented this" )

    # switches to the next set of objects
    def switchObjects(self):
        raise NotImplementedError( "Should have implemented this" )
        
    # maybe use state objects? check out state design pattern...
    # we also have a more strict and simple state change diagram...
    def changeState(self, newState):
        raise NotImplementedError( "Should have implemented this" )

    # redo the given spot
    def redoTrial(self, trial):
        raise NotImplementedError( "Should have implemented this" )

    # maybe have update? for changing color of cylinders...
