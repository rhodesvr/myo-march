"""
 This class regulates the user.
 It creates step objects to populate its queue, which the exp consumes.
 It also provides a way to get the angle and other info from the user

 THIS IS THE CLASS WHICH MEASURES IF THE USER HAS TAKEN A STEP
"""

class NavSystem(object):
    # object which holds step events... make step events?
    stepQueue = []

    def getAngle(self):
        raise NotImplementedError( "Should have implemented this" )

    def produceStep(self):
        if hasStepped():
            # for now, we are just inserting angle
            # maybe later, include speed/distance?
            stepQueue.insert(0, getAngle())

    def hasStepped(self):
        raise NotImplementedError( "Should have implemented this" )

    def getStep(self):
        if len(stepQueue) > 0:
            return stepQueue.pop()
        else:
            raise Exception("stepqueue is empty")
