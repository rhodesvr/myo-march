using UnityEngine;
using System.Collections;
using LockingPolicy = Thalmic.Myo.LockingPolicy;
using Pose = Thalmic.Myo.Pose;
using UnlockType = Thalmic.Myo.UnlockType;
using VibrationType = Thalmic.Myo.VibrationType;

public class CameraHolderScript : MonoBehaviour {
    public float speed;
    public float height;
    private Rigidbody rb;
    private GameObject mainCamera;
    public LocomotionInterface locomotion;

    private Vector3 previous;

    // Use this for initialization
    void Start () {
        // why do we need rigid body? Can't we just use our own position?
        rb = GetComponent<Rigidbody>();
        
        transform.position = new Vector3(0.0f, height, 0.0f);
        mainCamera = GameObject.Find("Main Camera");
    }

    // x is the forward direction
    void LateUpdate()
    {
        //Debug.Log(thalmicMyo.gyroscope);
        float y = mainCamera.transform.eulerAngles.y;
        
        float moveAmount = locomotion.getMovement(speed);
        Vector3 newMove = new Vector3(
            Mathf.Sin(y * Mathf.Deg2Rad) * moveAmount,
            0.0f,
            Mathf.Cos(y * Mathf.Deg2Rad) * moveAmount)
        ;
        rb.transform.Translate(newMove);        
        
    }
}
