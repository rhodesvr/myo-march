using UnityEngine;
using UnityEngine.UI;
using System.Collections;


// this is the class which includes the majority of the experiment logic!
public class Main : MonoBehaviour {

    public string userInitial;
    public int userId;
    public CameraHolderScript oculusHolder;
    public Material blackMaterial;
    public GameObject orientationMarker;
    public GameObject locationMarker;
    public GameObject avatar;
    public ObjectController objectController;
    // these are the different locomotion methods to test in our experiment
    int[] locomotionMethodsOrder;
    public LocomotionInterface[] locomotionMethods;

    private int locomotionIndex;
    private const long TICKS_PER_SECOND = 10000000;
    private Material skyBoxMaterial;
    private string output;

    public Text onGuiString;

    private int FALLBACK_EXPERIMENT_INDEX;

    // different orders of running through locomotions
    int[][] locomotionMethodsOrders = new int[6][]
    {
        new int[3] {0,1,2 },
        new int[3] {0,2,1 },
        new int[3] {1,0,2 },
        new int[3] {1,2,0 },
        new int[3] {2,0,1 },
        new int[3] {2,1,0 }
    };
    

    // Use this for initialization
    void Start () {
        onGuiString.text = "explore";
        locomotionIndex = 0;
        locomotionMethodsOrder = locomotionMethodsOrders[userId % locomotionMethodsOrders.Length];
        Debug.Log("running through locomotions in order [" + locomotionMethods[locomotionMethodsOrder[0]] +
            ", " + locomotionMethods[locomotionMethodsOrder[1]] + ", " + locomotionMethods[locomotionMethodsOrder[2]] + "]");

        
        if (locomotionMethods.Length != locomotionMethodsOrder.Length)
            throw new System.Exception("sizes do not align!");

        // open a file to store the results
        output = "trial number, correct angle (degrees), angle diff (degrees), latency (ticks)\n";
        // overwrite default locomotion method in OculusHolder
        oculusHolder.locomotion = locomotionMethods[locomotionMethodsOrder[locomotionIndex]];
        possiblyActivatePPT();

        scriptOut("starting with navigation method" + oculusHolder.locomotion);

        objectController.setId(userId);
        ExperimentUtilities.hideObjectChildren(avatar);
        ExperimentUtilities.hideObjectChildren(locationMarker);
        ExperimentUtilities.hideObjectChildren(orientationMarker);
        FALLBACK_EXPERIMENT_INDEX = 0;
    }
    

    /**
     * For a locomotion method,
     * test all of the trials within it.
     */
    IEnumerator testLocomotionMethod(int currentExperimentIndex)
    {
        Debug.Log("let the user move around a little");
        yield return StartCoroutine(waitForSpace());
        // show the cylinder, etc,
        ExperimentUtilities.showObjectChildren(getCylinder());
        ExperimentUtilities.showObjectChildren(getArrow());
        yield return StartCoroutine(waitForSpace());
        Debug.Log("and we begin the real experiment");

        int numLocations = getNumLocations();
        for (int i = 0; i < numLocations; i ++)
        {
            // get location bundle from object controller
            ObjectController.LocationInformation info = objectController.getLocationInformation(currentExperimentIndex, i);
            // update cylinder and arrow location, maybe pass these as arguments instead
            locationMarker.transform.position = info.locationObjectLocation;
            orientationMarker.transform.position = info.orientationObjectLocation;
            yield return StartCoroutine(testLocation(currentExperimentIndex, i, info.objectsToFace, info.objectNames));
        }

        
        yield return new WaitForEndOfFrame();
    }

    void shuffle(float[] fs)
    {
        for (int i = 0; i < fs.Length; i ++)
        {
            float temp = fs[i];
            int r = Random.Range(i, fs.Length);
            fs[i] = fs[r];
            fs[r] = temp;
        }
    }

    /**
     * Way of testing more than a user's spatial orientation given a locomotion method
     */
    IEnumerator testBlindWalking(int currenExperimentIndex)
    {            
        // hide all current objects, including cylinder and arrow
        ExperimentUtilities.hideObjectChildren(locationMarker);
        ExperimentUtilities.hideObjectChildren(orientationMarker);
        ExperimentUtilities.showObjectChildren(avatar);
        objectController.hideCurrentObjects(currenExperimentIndex);
        output += "===\n";

        float[] distances = { 10,10,20,20,30,30,40,40};
        shuffle(distances);
        for (int distanceIndex = 0; distanceIndex < distances.Length; distanceIndex ++)
        {
            
            // move user to middle of stage
            scriptOut("move user to place for blind walking");
            yield return StartCoroutine(waitForSpace());
            // hopefully this isn't an issue when we do blind walking with oculus
            oculusHolder.transform.position = new Vector3(0, oculusHolder.baseHeight + oculusHolder.userHeight, 0);
            // place avatar in front of them
            avatar.transform.position = getAvatarTransform(distances[distanceIndex],Mathf.Deg2Rad * getViewAngle());
            avatar.transform.Rotate(0.0f, 180f, 0.0f);
            ExperimentUtilities.showObjectChildren(avatar);
            scriptOut("please walk to the avatar (space when done saying)");
            yield return StartCoroutine(waitForSpace());

            // when they say, record information then turn screen off
            turnOffScenery();
            ExperimentUtilities.hideObjectChildren(avatar);
            Vector3 startPos = oculusHolder.transform.position;
            long startTime = System.DateTime.Now.Ticks;

            // when they think they are there, record distance and output to file
            yield return StartCoroutine(waitForSpace());
            // but we don't need this! need the distance from the avatar!
            Vector3 endPos = oculusHolder.transform.position;
            float sign = getSign(Mathf.Deg2Rad * getViewAngle());
            float diff = (endPos.z - avatar.transform.position.z) * sign;
            long endTime = System.DateTime.Now.Ticks; // 10,000 ticks in a millisecond
            turnOnScenery();
            oculusHolder.transform.position = new Vector3(0, oculusHolder.baseHeight + oculusHolder.userHeight, 0);
            output += getBlindWalkingOutput(locomotionMethodsOrder[locomotionIndex], distances[distanceIndex], diff, endTime - startTime);
            yield return new WaitForEndOfFrame();
        }
        ExperimentUtilities.showObjectChildren(locationMarker);
        ExperimentUtilities.showObjectChildren(orientationMarker);
        ExperimentUtilities.hideObjectChildren(avatar);
        output += "===\n";
        // don't need to show current objects because we have new ones now!
    }
    float getSign(float angle)
    {
        return Mathf.Sin(angle) / Mathf.Abs(Mathf.Sin(angle));
    }
    Vector3 getAvatarTransform(float d, float angle)
    {
        float sign = getSign(angle);
        return new Vector3(0, 0, d * sign);
    }

    // get a location from the object manager, move to cylinder, face arrow, then do the objects!
    IEnumerator testLocation(int currentExperimentIndex, int trialIndex, GameObject[] objectsToTurnToFace, string[] namesOfObjectsToFace)
    {
        GameObject cylinder = getCylinder();
        GameObject arrow = getArrow();

        // TODO display the cylinder and arrow
        // wait for user to navigate to cylinder
        scriptOut("please move to the cylinder");
        yield return StartCoroutine(waitForSpace());

        switchSpeeds();
        ExperimentUtilities.hideObjectChildren(cylinder);

        // turn the screen off but arrow and cylinder
        // turnOffScenery();
        objectController.hideCurrentObjects(currentExperimentIndex);
        
        int numObjectsPerLocation = getNumObjectsPerLocation();

        for (int i = 0; i < objectsToTurnToFace.Length; i ++)
        {
            
            // wait for user to turn to the arrow, then turn off cylinder
            scriptOut("please turn to face the sphere");
            yield return StartCoroutine(waitForSpace());

            GameObject objectLocation = objectsToTurnToFace[i];
            // say turn to face the certain object
            scriptOut("please turn to face the " + 
                namesOfObjectsToFace[i] + " (push space when done saying)");
            yield return StartCoroutine(waitForSpace());

            // get correct angle
            float correctAngle = getAngleDiff(objectLocation);

            // remove the arrow
            ExperimentUtilities.hideObjectChildren(arrow);

            // record initial time
            long startTime = System.DateTime.Now.Ticks;
            // they turn to face object and say okay
            yield return StartCoroutine(waitForSpace());
            
            // record end time to find latency
            long endTime = System.DateTime.Now.Ticks;
            long diffTicks = endTime - startTime;
            long diffSeconds = diffTicks;

            // compute correct angle/ angle diff
            float angleDiff = getAngleDiff(objectLocation);
            Debug.Log("correct relative angle between arrow and object was " + correctAngle);
            Debug.Log("and their global angle was " + getViewAngle()); // sometimes incorrect? check out blue
            Debug.Log("they were off by: " + angleDiff);
            Debug.Log("and they took: " + diffSeconds + "(in ticks)");

            // output everything necessary
            output += getOutput(locomotionMethodsOrder[locomotionIndex], trialIndex,
                correctAngle, angleDiff, diffSeconds);

            // show the arrow again
            ExperimentUtilities.showObjectChildren(arrow);
            // ask them to face the arrow

        } // done with objects at location
        scriptOut("please turn to face the sphere");
        yield return StartCoroutine(waitForSpace());
        // turn the entire screen on
        // turnOnScenery();
        objectController.showCurrentObjects(currentExperimentIndex);

        // reset speed as moving away from location
        switchSpeeds();

        // remove arrow, cylinder from screen
        // this is interesting-- should we destroy them? just make them invisible?
        ExperimentUtilities.hideObjectChildren(arrow);

        yield return new WaitForEndOfFrame();
    }

    float previousSpeed = 0;
    void switchSpeeds()
    {
        float temp = oculusHolder.speed;
        oculusHolder.speed = previousSpeed;
        previousSpeed = temp;
    }

    public float getAngleDiff(GameObject obj)
    {
        return VEMath.angleDiff(
            getActualAngle(obj),
            getViewAngle())
            ;
    }

    public float getViewAngle()
    {
        return VEMath.eulerAngleToCoordinateAngle(
            getCamera().transform.eulerAngles.y);
    }

    // should return actual angle between these two objects
    float getActualAngle(GameObject other)
    {
        return VEMath.getAngle3D(
            getCamera().transform.position,
            other.transform.position);
    }

    int getNumExperiments()
    {
        return locomotionMethods.Length;
    }

    // TODO we need to tie this to object manager somehow
    int getNumLocations()
    {
        return 6;
    }
    // TODO this should also be tied to object manager
    int getNumObjectsPerLocation()
    {
        return 3;
    }

    void scriptOut(string s)
    {
        onGuiString.text = s;
    }
    /**
    As betsy says,
        the correct angle of response, turning error, and latency are all important
        */
    string getOutput(int trialNum, int trialIndex, float correctResponse, float angleDiff, long tickDiff)
    {
        string endLine = "\n";
        string delimter = ", ";
        return "" + trialNum + delimter + trialIndex + delimter +
            correctResponse + delimter + angleDiff + delimter + tickDiff + endLine;
    }

    string getBlindWalkingOutput(int trialIndex, float correct, float delta, long tickdiff)
    {
        string endLine = "\n";
        string delimter = ", ";
        return "" + trialIndex + delimter + correct + delimter + delta + delimter + tickdiff + endLine;
    }

    void outputToFile(string o)
    {
        scriptOut("outputted to file");
        string path = ".\\" + userInitial + "_results" + userId + ".txt";
        System.IO.File.WriteAllText(path, o);
    }
    void turnOffScenery()
    {
        // get all objects with the scenery tag
        GameObject[] toHide = GameObject.FindGameObjectsWithTag("Scenery");

        // for all objects
        foreach (GameObject obj in toHide)
        {
            ExperimentUtilities.hideObjectChildren(obj);
        }

        // strangely enough, there is still something left... 
        // so we use fog to cover the rest up
        skyBoxMaterial = RenderSettings.skybox;
        RenderSettings.skybox = blackMaterial;
        //RenderSettings.fog = true;
        
    }
    
    // could try to use tagging here?
    void turnOnScenery()
    {
        GameObject[] toShow = GameObject.FindGameObjectsWithTag("Scenery");
        foreach(GameObject obj in toShow)
        {
            ExperimentUtilities.showObjectChildren(obj);
        }
        RenderSettings.skybox = skyBoxMaterial;
        //RenderSettings.fog = false;
    }
    GameObject getCylinder()
    {
        ExperimentUtilities.showObjectChildren(locationMarker);
        return locationMarker;
    }
    GameObject getArrow()
    {
        ExperimentUtilities.showObjectChildren(orientationMarker);
        return orientationMarker;
    }
    
    Camera getCamera()
    {
        return oculusHolder.GetComponentInChildren<Camera>();
    }
    // Update is called once per frame
    void Update () {
        if (Input.GetKeyDown("h"))
            turnOffScenery();
        if (Input.GetKeyDown("s"))
            turnOnScenery();
        if (Input.GetKeyDown("c"))
        {
            outputToFile(output);
        }
        if (Input.GetKeyDown("b"))
        {
            switchSpeeds();
        }
        if (Input.GetKeyDown("l"))
        {
            StartCoroutine("testLocomotion");
        }
        if (Input.GetKeyDown("w"))
        {
            StartCoroutine("testWalking");
        }
        if (Input.GetKeyDown("m"))
        {
            updateLocomotion();
            // update objects too
            objectController.progressToNewExperiment();
            FALLBACK_EXPERIMENT_INDEX= (FALLBACK_EXPERIMENT_INDEX + 1) % 3;
        }
        for (int i = 1; i < 7; i++)
        {
            if (Input.GetKeyDown(""+ (char)('0' + i)))
            {
                scriptOut("redoing " + i);
                output += "redoing " + i + "\n";
                StartCoroutine("redoTrial", (i - 1));
            }
        }
    }
    
    IEnumerator testLocomotion()
    {
        print("trying to test locomotion");
        scriptOut("testing locomotion");
        yield return StartCoroutine(testLocomotionMethod(FALLBACK_EXPERIMENT_INDEX));
        
    }
    IEnumerator testWalking()
    {
        // now that we are done with the spatial orientation tasks, start blind walking
        yield return StartCoroutine(testBlindWalking(FALLBACK_EXPERIMENT_INDEX));
    }
    

    IEnumerator redoTrial(int toRedo)
    {
        // get location bundle from object controller
        ObjectController.LocationInformation info = objectController.getLocationInformation(FALLBACK_EXPERIMENT_INDEX, toRedo);
        // update cylinder and arrow location, maybe pass these as arguments instead
        locationMarker.transform.position = info.locationObjectLocation;
        orientationMarker.transform.position = info.orientationObjectLocation;
        yield return StartCoroutine(testLocation(FALLBACK_EXPERIMENT_INDEX, toRedo, info.objectsToFace, info.objectNames));
    }
    /**
     * Switches between locomotion methods in public array
     */
    void updateLocomotion()
    {
        locomotionIndex = (locomotionIndex + 1) % locomotionMethods.Length;
        
        oculusHolder.locomotion = locomotionMethods[locomotionMethodsOrder[locomotionIndex]];

        possiblyActivatePPT();
        Debug.Log("now using " + oculusHolder.locomotion);
    }

    void possiblyActivatePPT()
    {
        PPTLocomotion.active = oculusHolder.locomotion.GetType() == typeof(PPTLocomotion);
    }
    

    IEnumerator waitForSpace()
    {
        // while we haven't pressed space, keep on waiting
        while (!Input.GetKeyDown("space"))
        {
            //Debug.Log("We pressed space!");
            yield return null;

        }
        Debug.Log("done with wait for space");
        yield return new WaitForEndOfFrame();

    }
}
