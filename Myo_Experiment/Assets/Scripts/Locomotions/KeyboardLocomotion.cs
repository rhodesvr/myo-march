using UnityEngine;
using System.Collections;
using System;

public class KeyboardLocomotion : LocomotionInterface {

    public override float getMovement(float speed)
    {
        if (Input.GetKeyDown("up"))
            return speed;
        else
            return 0;
    }

    // Use this for initialization
    void Start () {
        Debug.Log("starting keyboard locomotion");
	}
	
	// Update is called once per frame
	void Update () {
	
	}
}
