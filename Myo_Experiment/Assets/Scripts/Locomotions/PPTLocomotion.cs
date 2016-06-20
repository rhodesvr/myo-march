using UnityEngine;
using System.Collections;
using System;
using System.IO;







public class PPTLocomotion : LocomotionInterface {
    private byte[] a;
    private Vector3 position;
    private Vector3 old;
    public static Boolean active;
    public float scalar;
    public float startingAngle;
    public CameraHolderScript oculusHolder;
    int goodCount, errorcount, framecount;
    public override float getMovement(float speed)
    {
        return 0;
    }

    // Use this for initialization
    void Start()
    {
        Debug.Log("trying to start ppt locomotion");
        
        goodCount = 0; errorcount = 0; framecount = 0;
        startingAngle = oculusHolder.mainCamera.transform.eulerAngles.y;
    }
	
	// Update is called once per frame
	void Update () {
        if (active)
        {
            if (framecount > 60)
            {
                framecount = 0;
                goodCount = 0;
                errorcount = 0;
            }
            framecount++;
            //print(goodCount + " : " + errorcount);

            try
            {
                // note that this always looks for this in the project root directory
                a = System.IO.File.ReadAllBytes("coordinates.txt");
                // decode a and turn into 3 floats
                string result = System.Text.Encoding.UTF8.GetString(a);
                String[] pos = result.Split(',');

                Debug.Log(result);

                // print(pos[0] + "," + pos[1] + "," + pos[2]);
                position.z = /*-1 * Mathf.Cos(Mathf.Deg2Rad * startingAngle)**/
                    Convert.ToSingle(pos[2]) * scalar;
                // print(position.x);
                position.y = oculusHolder.baseHeight + Convert.ToSingle(pos[1]);
                position.x = /*Mathf.Cos(Mathf.Deg2Rad * startingAngle) **/
                    Convert.ToSingle(pos[0]) * scalar;
                // print(position);
                oculusHolder.transform.position = position;
                old = position;
                goodCount++;


            }
            catch (Exception e)
            {
                errorcount++;
                // sharing violation!
            }
        }
    }
}
