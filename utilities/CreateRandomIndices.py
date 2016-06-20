'''
Create and output the random indices
for locations as well as the order of which objects to face.
'''

from itertools import permutations
import random

orderingsDic = {  }
def getOrderings(n):
    if n not in orderingsDic:
        indices = range(n)
        orderingsDic[n] = list(permutations(indices))

    # now that we have permutations, get a random index of permutations
    perms = orderingsDic[n]
    randIndex = random.randrange(len(perms))
    return perms[randIndex]

def main(locationArrayName="locations", objectIndexArrayName="object"):
    numLocations = 6
    numParticipants = 12
    numObjectsPerLocation = 3
    
    # get 12 different orders of visiting 6 locations
    locationOrderings = [getOrderings(numLocations) for x in range(numParticipants)]

    objectIndexOrderings = [\
                            [getOrderings(numObjectsPerLocation) for y in range(numLocations)] \
                            for x in range(numParticipants)]

    print("location orderings:")
    for indices in locationOrderings:
        print(indices)
        
    print("objectIndexOrderings:")
    for indices in objectIndexOrderings:
        print(indices)

    locationBase = "new int[" + str(numLocations) + "]"
    locationSubstring = locationBase + listToArrayString(locationOrderings[0])
    for indices in locationOrderings[1:]:
        locationSubstring += ",\n" + locationBase + listToArrayString(indices)
    locationsString = locationArrayName + " = new int[" + str(numParticipants) + \
                      "][]{\n" + locationSubstring + "\n};"

    print(locationsString)
    # and now do a similar thing for orderings
    objectBase = "new int[" + str(numObjectsPerLocation) + "]"
    objectBase2 = "new int[" + str(numLocations) + "][" + str(numObjectsPerLocation) + "]"
    objectSubstring = ""
    for i in range(numParticipants):
        objectSubstring += objectBase2 + "{"
        for j in range(numLocations):
            objectSubstring += "new int[3]" + \
                               listToArrayString(objectIndexOrderings[i][j]) +\
                               ", "
        objectSubstring += "},\n"
    objectString = objectIndexArrayName + " = new int[" + str(numParticipants)\
                   + "][" + str(numLocations) + "]["\
                   + str(numObjectsPerLocation) + "]{\n" + objectSubstring + "\n};"

    print(objectString)

def listToArrayString(lst):
    ret = "{" + str(lst[0])
    for i in lst[1:]:
        ret += ", " + str(i)
    return ret + "}"
main()
