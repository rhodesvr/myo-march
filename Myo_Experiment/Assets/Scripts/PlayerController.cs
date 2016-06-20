using UnityEngine;
using System.Collections;

using LockingPolicy = Thalmic.Myo.LockingPolicy;
using Pose = Thalmic.Myo.Pose;
using UnlockType = Thalmic.Myo.UnlockType;
using VibrationType = Thalmic.Myo.VibrationType;


public class PlayerController : MonoBehaviour {

	public float speed;
	public float gyro_mult;

	private Rigidbody rb;

	public GameObject myo;

    public float jitterBoundary;

    private float previous;


	void Start() {
		rb = GetComponent<Rigidbody> ();
        previous = myo.GetComponent<ThalmicMyo>().gyroscope.z;
	}
	
	void FixedUpdate () {
        // should move this stuff to camera holder script, but good to test here!
		ThalmicMyo thalmicMyo = myo.GetComponent<ThalmicMyo> ();

		//Debug.Log (thalmicMyo.gyroscope); 

		float movement = thalmicMyo.gyroscope.z;

        float diff = previous - movement;
        previous = movement;

        // make sure that we don't jitter
        if (diff > jitterBoundary) 
            rb.transform.Translate(0, 0, Mathf.
                Abs(diff * speed), Space.Self);
	}

	void OnTriggerEnter(Collider other) {
		if (other.gameObject.CompareTag ("Pick Up")) {
			other.gameObject.SetActive (false);

		}
	}
}
