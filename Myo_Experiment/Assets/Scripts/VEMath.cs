using UnityEngine;
using System.Collections;

public class VEMath : MonoBehaviour {

	// Use this for initialization
	void Start () {
	
	}
	
	// Update is called once per frame
	void Update () {
	
	}

    /**
     * given two angles in degrees, return the difference between them
     */
    public static float angleDiff(float a1, float a2)
    {
        float smaller = (a1 < a2) ? a1 : a2;
        float larger = (a1 > a2 ) ? a1 : a2;

        float d1 = larger - smaller;
        float d2 = smaller + 360.0f - larger;

        return Mathf.Min(d1, d2);
    }

    /**
     * given two positions, return the 2d (xz) angle between them in degrees
     */
    public static float getAngle2D(Vector2 a, Vector2 b)
    {
        float hypotenuse = (b - a).magnitude;
        float adjacent = b.x - a.x;
        float opposite = b.y - a.y;

        bool debug = false;
        if (debug)
        {
            Debug.Log("here is a " + a);
            Debug.Log("here is b: " + b);
            Debug.Log("hypotenuse: " + hypotenuse);
            Debug.Log("adjacent: " + adjacent);
        }
        float theta1 = 0;
        try
        {
            // remember this is restricted to [0, 180]
            theta1 = Mathf.Acos(adjacent / hypotenuse);
        }
        catch (System.DivideByZeroException ex)
        {
            Debug.Log("We tried to divide by zero in getAngle2d" + ex.Data);
            return theta1;
        }
        

        return angleToPositiveAngle(((opposite > 0)? 1: -1) *Mathf.Rad2Deg * theta1);
    }

    // same as above, but given two vector3d's
    public static float getAngle3D(Vector3 a, Vector3 b)
    {
        return getAngle2D(new Vector2(a.x, a.z), new Vector2(b.x, b.z));
    }

    /**
     * Given an euler angle in degrees (usually from the camera's view),
     * convert it to the correct coordinate angle.
     * As motivation, the euler angle when facing the z direction
     * is 0 degrees, when it should be 90 if the x axis is
     * itself and the z axis is the y axis in 2d.
     * We can either change the euler angle or change our math--
     * this is a variation where we changed the angle.
     */
    public static float eulerAngleToCoordinateAngle(float y)
    {
        float temp = -y + 90;
        // is this is faster than (-y + 450) % 360? or use a ternary operator and addition?
        return angleToPositiveAngle(temp);
    }

    public static float angleToPositiveAngle(float y)
    {
        return (y + 360) % 360;
    }
}
