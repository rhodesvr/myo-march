using UnityEngine;
using System.Collections;
using System;

public class TwoMyoMarchLocomotion : LocomotionInterface {

    public GameObject myo;
    public GameObject myo2;

    public float scalingFactor;

    private float previous1, previous2;

	// Use this for initialization
	void Start () {
        Debug.Log("starting myo march locomotion");
        previous1 = myo.GetComponent<ThalmicMyo>().transform.forward.y;
        previous2 = myo.GetComponent<ThalmicMyo>().transform.forward.y;
	}
	
	// Update is called once per frame
	void Update () {
	
	}

    public override float getMovement(float speed)
    {
        bool debug = false;
        ThalmicMyo thalmicMyo = myo.GetComponent<ThalmicMyo>();
        ThalmicMyo otherMyo = myo2.GetComponent<ThalmicMyo>();

        float ypos1 = thalmicMyo.transform.forward.y;
        float ypos2 = otherMyo.transform.forward.y;
        if (debug)
            Debug.Log(ypos1 + "," + ypos2);

        float diff1 = Mathf.Abs(ypos1 - previous1);
        float diff2 = Mathf.Abs(ypos2 - previous2);

        previous2 = ypos2;
        previous1 = ypos1;

        return (diff1 + diff2) * speed * scalingFactor;
    }
}
