"""
 This class contains the logic of the experiment,
 including obtaining results,
 defining the correct env and nav device,
 and moving the env through the different stages of the exp
"""

class KinectExperiment(Experiment):
    subjectID = -1
    def initSubjectID(self):
        validID = False
        while not (validID):
            try:
                #Prompt the user for an ID number
                subjectID = int(viz.input('Input Subject ID Number'))
                RESULTS_DIRECTORY = 'C:\Users\Administrator\Downloads'
                #Validate the subject ID number
                outFilePath = '%s\Subject_%s.txt' %(RESULTS_DIRECTORY, str(subjectID))
                if os.path.exists(outFilePath) or subjectID is '':
                    yes = viz.ask('The Subject ID Number ' + str(subjectID) + ' already exists. Pick a new one?')
                        if not yes:
                            raise 'Exiting...'
                else:
                    validID = True
                    print "we have a valid ide!"
            except ValueError:
                print('Subject ID number must be an integer')

        
    environment = 0
    def setEnvironment(self, env):
        environment = env
    # have an array of navigation systems?
    navigation = 0
    def setNavigationSystem(self, nav):
        navigation = nav

    conditions = []
    conditionIndex = -1
    def changeConditions(self):
        raise NotImplementedError( "Should have implemented this" )

    startTime = 0

    resultFile = 0
    # this will be an interesting function to write...
    # maybe split it up into starting a spot,
    # starting an object, etc...
    # or should env handle that?
    def getResult(self):
        raise NotImplementedError( "Should have implemented this" )

    # consumes a step off of navigation's step queue
    def consumeStep(self):
        raise NotImplementedError( "Should have implemented this" )

    # this can be entry point for program
    def start():
        viz.go(viz.PROMPT)

def main():
    # instantiate a new KinectExperiment
    # maybe could even move this to its own class...
    # can we still use the name/main trick?
