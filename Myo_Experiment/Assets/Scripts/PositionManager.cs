using UnityEngine;
using System.Collections;

public class PositionManager : MonoBehaviour {
    public Material closeMaterial;
    public Material elseMaterial;
    public Camera view;
    public float boundaryDistance;

    private bool changedTexture;
    private Renderer r;

	// Use this for initialization
	void Start () {
        changedTexture = false;
        r = GetComponent<Renderer>();
        r.material = elseMaterial;
	}
	
    bool closeEnough()
    {
        //Debug.Log((view.transform.position - transform.position).magnitude);
        Vector3 diff = view.transform.position - transform.position;
        diff.y = 0;
        return (diff).magnitude < boundaryDistance;
    }

	// Update is called once per frame
	void Update () {
        // if we are close enough,
	    if (closeEnough()) {
            // change the material to something else!
            r.material = closeMaterial;
            changedTexture = true;
        }

        // if we are not close enough and texture has changed
        else if (changedTexture)
        {
            r.material = elseMaterial;
            changedTexture = false;
        }
        // should probably have something here to switch back
	}
}
