using UnityEngine;
using System.Collections;
using System;

public class MyoMarchLocomotion : LocomotionInterface {

    public GameObject myo;

    public float scalingFactor;

    private Vector3 previous;

	// Use this for initialization
	void Start () {
        Debug.Log("starting myo march locomotion");
        previous = myo.GetComponent<ThalmicMyo>().transform.forward;
	}
	
	// Update is called once per frame
	void Update () {
	
	}

    public override float getMovement(float speed)
    {
        bool debug = false;
        ThalmicMyo thalmicMyo = myo.GetComponent<ThalmicMyo>();

        Vector3 current = thalmicMyo.transform.forward;

        Vector3 diff = current - previous;
        previous = current;

        if (debug)
            Debug.Log("here is diff: " + diff.magnitude);

        return diff.magnitude;
    }
}
