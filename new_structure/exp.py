"""
 This class contains the logic of the experiment,
 including obtaining results,
 defining the correct env and nav device,
 and moving the env through the different stages of the exp
====
 What about if something contains multiple parts in an experiment?
 Something like testing spatial orientation and perceived distance??
"""

class Experiment(object):
    subjectID = -1
    subjectInitial = 't'
    environment = 0
    # have an array of navigation systems?
    navigation = 0
    conditions = []
    conditionIndex = -1
    startTime = 0

    resultFile = 0
    def initSubjectID(self):
        raise NotImplementedError( "Should have implemented this" )
    def initSubjectInitial(self):
        raise NotImplementedError( "Should have implemented this" )
    def setEnvironment(self, env):
        environment = env
    def setNavigationSystem(self, nav):
        navigation = nav

    # maybe change this to change navigation?
    def changeConditions(self):
        raise NotImplementedError( "Should have implemented this" )

    # this will be an interesting function to write...
    # maybe split it up into starting a spot,
    # starting an object, etc...
    # or should env handle that?
    def getResult(self):
        raise NotImplementedError( "Should have implemented this" )

    # consumes a step off of navigation's step queue
    def consumeStep(self):
        raise NotImplementedError( "Should have implemented this" )
