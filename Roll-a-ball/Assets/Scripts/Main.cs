using UnityEngine;
using System.Collections;


// this is the class which includes the majority of the experiment logic!
public class Main : MonoBehaviour {

    delegate void del();
    public string userInitial;
    public CameraHolderScript oculusHolder;
    public Material blackMaterial;
    public GameObject tempArrow;
    public GameObject tempObject;
    // these are the different locomotion methods to test in our experiment
    public int[] locomotionMethodsOrder;
    public LocomotionInterface[] locomotionMethods;

    private int locomotionIndex;
    private const long TICKS_PER_SECOND = 10000000;
    private Material skyBoxMaterial;
    private string output;


    // Use this for initialization
    IEnumerator Start () {
        locomotionIndex = 0;
        if (locomotionMethods.Length != locomotionMethodsOrder.Length)
            throw new System.Exception("sizes do not align!");

        // open a file to store the results
        output = "trial number, object number, angle diff (degrees), latency (ticks)\n";
        // overwrite default locomotion method in OculusHolder
        oculusHolder.locomotion = locomotionMethods[locomotionMethodsOrder[locomotionIndex]];

        Debug.Log("starting with navigation method" + oculusHolder.locomotion);

        yield return StartCoroutine(beginExperiment());
        Debug.Log("done with experiment");
        outputToFile(output);
    }

    /**
     * This does the experiment over however many locomotion methods we have
     */
    IEnumerator beginExperiment()
    {
        int numExperiments = getNumExperiments();

        for (int i = 0; i < numExperiments; i ++)
        {
            yield return StartCoroutine(testLocomotionMethod());
            updateLocomotion();
            // update objects too
            // move user back to starting location?
        }
    }

    /**
     * For a locomotion method,
     * test all of the trials within it.
     */
    IEnumerator testLocomotionMethod()
    {
        Debug.Log("let the user move around a little");
        yield return StartCoroutine(waitForSpace());
        Debug.Log("and we begin the real experiment");

        int numLocations = getNumLocations();
        for (int i = 0; i < numLocations; i ++)
        {
            yield return StartCoroutine(testLocation());
        }
        yield return new WaitForEndOfFrame();
    }

    // get a location from the object manager, move to cylinder, face arrow, then do the objects!
    IEnumerator testLocation()
    {
        GameObject cylinder = getCylinder();
        GameObject arrow = getArrow();

        // TODO display the cylinder and arrow
        // wait for user to navigate to cylinder
        Debug.Log("please move to the cylinder");
        yield return StartCoroutine(waitForSpace());

        // once they are there, set their speed to zero so they don't move
        float previousSpeed = oculusHolder.speed;
        oculusHolder.speed = 0;

        // turn the screen off but arrow and cylinder
        turnOffScenery();
        
        int numObjectsPerLocation = getNumObjectsPerLocation();

        for (int i = 0; i < numObjectsPerLocation; i ++)
        {
            
            // wait for user to turn to the arrow, then turn off cylinder
            Debug.Log("please turn to face the arrow");
            yield return StartCoroutine(waitForSpace());

            GameObject objectLocation = getCurrentObject();
            // say turn to face the certain object
            Debug.Log("please turn to face the object (push space when done saying)");
            yield return StartCoroutine(waitForSpace());

            // remove the arrow
            hideObject(arrow);

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
            Debug.Log("they were off by: " + angleDiff);
            Debug.Log("and they took: " + diffSeconds + "(in ticks)");

            // output everything necessary
            output += getOutput(0, 0, angleDiff, diffSeconds);

            // show the arrow again
            showObject(arrow);
            // ask them to face the arrow

        } // done with objects at location

        // turn the entire screen on
        turnOnScenery();

        // reset speed as moving away from location
        oculusHolder.speed = previousSpeed;

        // remove arrow, cylinder from screen
        // this is interesting-- should we destroy them? just make them invisible?

        yield return new WaitForEndOfFrame();
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
    float getActualAngle(GameObject other)
    {
        return VEMath.getAngle3D(getCamera().transform.position,
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

    string getOutput(int trialNum, int objectNum, float angleDiff, long tickDiff)
    {
        string endLine = "\n";
        string delimter = ", ";
        return "" + trialNum + delimter + objectNum + delimter + angleDiff + delimter + tickDiff + endLine;
    }

    void outputToFile(string o)
    {
        string path = ".\\" + userInitial + "_results.txt";
        System.IO.File.WriteAllText(path, o);
    }
    void turnOffScenery()
    {
        // get all objects with the scenery tag
        GameObject[] toHide = GameObject.FindGameObjectsWithTag("Scenery");

        // for all objects
        foreach (GameObject obj in toHide)
        {
            hideObject(obj);
        }

        // strangely enough, there is still something left... 
        // so we use fog to cover the rest up
        skyBoxMaterial = RenderSettings.skybox;
        RenderSettings.skybox = blackMaterial;
        RenderSettings.fog = true;
        
    }

    void hideObject(GameObject toHide)
    {
        toHide.GetComponent<MeshRenderer>().enabled = false;
    }

    void showObject(GameObject toShow)
    {
        toShow.GetComponent<MeshRenderer>().enabled = true;
    }

    // could try to use tagging here?
    void turnOnScenery()
    {
        GameObject[] toShow = GameObject.FindGameObjectsWithTag("Scenery");
        foreach(GameObject obj in toShow)
        {
            showObject(obj);
        }
        RenderSettings.skybox = skyBoxMaterial;
        RenderSettings.fog = false;
    }
    GameObject getCylinder()
    {
        return null;
    }
    GameObject getArrow()
    {
        return tempArrow;
    }
    GameObject getCurrentObject()
    {
        return tempObject;
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
            outputToFile(output);
	}

    /**
     * Switches between locomotion methods in public array
     */
    void updateLocomotion()
    {
        locomotionIndex = (locomotionIndex + 1) % locomotionMethods.Length;
        oculusHolder.locomotion = locomotionMethods[locomotionMethodsOrder[locomotionIndex]];
        Debug.Log("now using " + oculusHolder.locomotion);
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
