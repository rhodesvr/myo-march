using UnityEngine;
/*
most of the functionality (of the angle calculation)
of this class is ripped away and placed in main.
It's kept around for historic reasons.
*/
public class OrientationManager : MonoBehaviour {
    public Material facingMaterial;
    public Material elseMaterial;
    public Camera view;
    public float viewRangeValue;

    private bool changedTexture;
    private Renderer r;

	// Use this for initialization
	void Start () {
        changedTexture = false;
        r = GetComponent<Renderer>();
	}

    // TODO: this is not taking into account where the oculus is facing
    bool cameraFacingThis()
    {
        bool debug = false;
        // there is the issue that adjustedY is bounded by acos's constraints
        float adjustedY = VEMath.eulerAngleToCoordinateAngle(view.transform.eulerAngles.y);
        float coordinateAngle = VEMath.getAngle3D(view.transform.position, transform.position);
        if (debug)
        {
            Debug.Log("here is our position: " + transform.position);
            Debug.Log("here is coordinateAngle " + coordinateAngle);
            Debug.Log("here is view's angle " + adjustedY);
        }
        return VEMath.angleDiff(
            coordinateAngle,
            adjustedY) 
            <= viewRangeValue;
    }

    public float getAngleDiff()
    {
        return VEMath.angleDiff(
            getActualAngle(),
            getViewAngle())
            ;
    }

    public float getViewAngle()
    {
        return VEMath.eulerAngleToCoordinateAngle(view.transform.eulerAngles.y);
    }
    public float getActualAngle()
    {
        return VEMath.getAngle3D(view.transform.position, transform.position);
    }
	
	// Update is called once per frame
	void Update () {
	    // if we are facing this object
        if (cameraFacingThis())
        {
            // change the material
            r.material = facingMaterial;
            changedTexture = true;
        }

        // else if we are not facing and have faced
        else if (changedTexture)
        {
            r.material = elseMaterial;
            changedTexture = false;
        }
	}
}
