using UnityEngine;
using System.Collections;
using System;
using System.Linq;
using System.Security.Cryptography;
//import RandomizedIndexManager;


public class ObjectController : MonoBehaviour{
    
    // this would be something like [[0,4,5],[...],...],
    // which means looking at objects 0, 4 and 5 at location 1
    // this does not change between subjects or locomotion methods
    int[][] indicesToTurnToFace;

    /** see index managers for the two below arrays**/
    // this designates the order in which we go to locations-> might need to be 3x6
    // this changes between subjects and between experiments
    int[] locationsOrder;
    // this represents the order in which we turn to face given indices in indicesToTurnToFace
    // for example, this would be something like [[0,2,1],[...],...]
    // which means that we would look at objects 0, 5, then 4 in the above indicesToTurnToFace example
    // changes between experiments and between subjects
    int[][] turnToFaceRandomizationIndices;

    int userId;
    int currentExperimentIndex;

    // maybe these two scales should be the same...
    public float positionScale; // 5 in vizard, don't think that will work here...
    public float objectScale;   // in case we want to scale where the objects are, default 1
    public float locationMarkerYPos;
    public float orientationMarkerYPos;
    public float distanceBetweenLocationAndOrientationMarkers; // .5 in vizard

    // locations of cylinders-- always the same
    Vector3[] locationMarkerLocations;
    // locations of arrows-- always the same
    Vector3[] orientationMarkerLocations;
    // will probably also need locations of objects-- always the same
    // or will this be part of the objects' information? 
    // will Ansel move objects to their locations?
    // or just move their proper locations here?
    Vector3[] objectLocations;
    public float objectHeight;
    public GameObject[] rawObjects;
    public string[] objectNames;

    /*
    Generic function, which given a location index and a list of objects,
    returns a subset of that list which corresponds to the transformed order
    of indicesToTurnToFace and turnToFaceRandomizationIndices
    */
    private T[] createRandomizedObjectList<T>(int locationIndex, T[] l, int rowIndex)
    {
        T[] ret = new T[3];

        for (int i = 0; i < 3; i ++)
        {
            int randomizedIndex = getRandomizedObjectIndex(locationIndex, i);
            ret[i] = l[rowIndex + randomizedIndex];
        }
        return ret;
    }
    

    private int getRandomizedObjectIndex(int currentLocationIndex, int i)
    {
        return indicesToTurnToFace[currentLocationIndex][turnToFaceRandomizationIndices[currentLocationIndex][i]];
    }

    private int getRandomLocationIndex(int currentIndex)
    {
        return locationsOrder[currentIndex];
    }
	
    public struct LocationInformation
    {
        public Vector3 locationObjectLocation, orientationObjectLocation;
        public GameObject[] objectsToFace;
        // this should line up with objects to face
        public string[] objectNames;
    }

    /**
     * @param int currentLocationIndex: represents which location we are at in experiment
     * this should increase linearly from 1..6
     * @return all information needed for this turn
     */
	public LocationInformation getLocationInformation (int currenExperimentIndex, int currentLocationIndex) {
        LocationInformation ret = new LocationInformation();
		int randomizedLocationIndex = getRandomLocationIndex(currentLocationIndex);
        ret.locationObjectLocation = locationMarkerLocations[randomizedLocationIndex];
        ret.orientationObjectLocation = orientationMarkerLocations[randomizedLocationIndex];
        if (objectNames == null)
            Debug.Log("here is our list of strings[" + objectNames.Length + "]: " + objectNames);
        // when we are actually working on experiment, change this zero to currenExperimentIndex
        ret.objectNames = createRandomizedObjectList<string>(randomizedLocationIndex, objectNames, currenExperimentIndex * 6);
        ret.objectsToFace = createRandomizedObjectList<GameObject>(randomizedLocationIndex, rawObjects, currenExperimentIndex * 6);

        return ret;
	}

    public void progressToNewExperiment()
    {
        currentExperimentIndex = (currentExperimentIndex + 1) % 3;
        // should we update locationorder indices and randomization indices?
        updateExperimentIndices(currentExperimentIndex);
        // also get the new objects here too!
        updateObjects(currentExperimentIndex * 6, 6);
    }

    public void updateExperimentIndices(int currIndex)
    {
        turnToFaceRandomizationIndices = RandomizedIndexManager.getTurnToFaceRandomizationIndices(userId, currIndex);
        locationsOrder = RandomizedIndexManager.getLocationOrderIndices(userId, currIndex);
    }

    public void updateObjects(int startIndex, int numObjects)
    {
        for (int i = 0; i < numObjects; i++)
        {
            // make previous object invisible
            int previousIndex = (i + startIndex + 12) % rawObjects.Length;
            ExperimentUtilities.hideObjectChildren(rawObjects[previousIndex]);

            // move current object to invisible's location
            rawObjects[i + startIndex].transform.position = objectLocations[i];
            ExperimentUtilities.showObjectChildren(rawObjects[i + startIndex]);
        }
    }

    public void hideCurrentObjects(int currentExperimentIndex)
    {
        for (int i = 0; i < 6; i++)
            ExperimentUtilities.hideObjectChildren(rawObjects[currentExperimentIndex * 6 + i]);
    }
    public void showCurrentObjects(int currentExperimentIndex)
    {
        for (int i = 0; i < 6; i++)
            ExperimentUtilities.showObjectChildren(rawObjects[currentExperimentIndex * 6 + i]);
    }
    void hideAllObjects()
    {
        foreach (GameObject obj in rawObjects)
        {
            ExperimentUtilities.hideObjectChildren(obj);
        }
    }
    
    // not currently used
    public void initObjects(GameObject[] objects, Vector3[] locations)
    {
        for (int i = 0; i < objects.Length; i ++)
        {
            objects[i].transform.position = locations[i];
        }
    }

    public void setId(int userId)
    {

        objectLocations = new Vector3[6]
        {
            new Vector3(-1.0408f * objectScale, objectHeight, 24f * objectScale),
            new Vector3(-8.44218f * objectScale, objectHeight, 4.5714f * objectScale),
            new Vector3(-15.2653f * objectScale, objectHeight, -9.90476f * objectScale),
            new Vector3(1.04082f * objectScale, objectHeight, -11.8095f * objectScale),
            new Vector3(12.6054f * objectScale, objectHeight, -21.7143f * objectScale),
            new Vector3(16.1122f * objectScale, objectHeight, -9.3283785f * objectScale)
        };
        
        hideAllObjects();
        this.userId = userId;
        currentExperimentIndex = -1;
        
        // get our specific ordering of viewing objects and visiting locations
        progressToNewExperiment();

        // might have to switch x and z coordinates on these...
        // update location and orientation thing
        // taken from myo2-- masterTargetLocations variable
        locationMarkerLocations = new Vector3[6] {
            new Vector3(-17f * positionScale,locationMarkerYPos,4f/3f * positionScale),
            new Vector3(-7.17007f * positionScale, locationMarkerYPos, -11.2381f * positionScale),
            new Vector3(1.04082f * positionScale,locationMarkerYPos,-20.8095f*positionScale),
            new Vector3(-18 * positionScale, locationMarkerYPos, 9 * positionScale),
            new Vector3(6.82313f * positionScale, locationMarkerYPos, -3.80952f * positionScale),
            new Vector3(15.2653f * positionScale, locationMarkerYPos, 7.47619f * positionScale)
        };
        // this is based on myo2-- master arrow locations
        // note that these are dependent on the placement of the location markers
        orientationMarkerLocations = new Vector3[6]
        {
            new Vector3(locationMarkerLocations[0].x,orientationMarkerYPos,locationMarkerLocations[0].z + distanceBetweenLocationAndOrientationMarkers),
            new Vector3(locationMarkerLocations[1].x + Mathf.Cos(Mathf.PI / 4.25f) * distanceBetweenLocationAndOrientationMarkers,
            orientationMarkerYPos,
            locationMarkerLocations[1].z + Mathf.Sin(Mathf.PI / 4.25f) * distanceBetweenLocationAndOrientationMarkers),
            new Vector3(locationMarkerLocations[2].x + distanceBetweenLocationAndOrientationMarkers,orientationMarkerYPos,locationMarkerLocations[2].z),
            new Vector3(locationMarkerLocations[3].x,orientationMarkerYPos,locationMarkerLocations[3].z - distanceBetweenLocationAndOrientationMarkers),
            new Vector3(locationMarkerLocations[4].x - distanceBetweenLocationAndOrientationMarkers,orientationMarkerYPos,locationMarkerLocations[4].z),
            new Vector3(locationMarkerLocations[5].x - distanceBetweenLocationAndOrientationMarkers,orientationMarkerYPos,locationMarkerLocations[5].z)
        };
        // update indicesToTurnToFace
        // this is taken from myo2-- masterTargetObjects variable
        indicesToTurnToFace = new int[6][]
        {
            new int[] {0,1,2 },
            new int[] {0,2,3 },
            new int[] {2,3,5 },
            new int[] {3,4,5 },
            new int[] {0,3,5 },
            new int[] {0,4,5 }
        };

    }
	
}
