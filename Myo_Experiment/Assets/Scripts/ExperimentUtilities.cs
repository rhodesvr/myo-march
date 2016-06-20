using UnityEngine;
using System.Collections;

public class ExperimentUtilities : MonoBehaviour {

	// Use this for initialization
	void Start () {
	
	}
	
	// Update is called once per frame
	void Update () {
	
	}

    public static void setRenderStateForObject(GameObject toDo, bool toWhat)
    {
        foreach (MeshRenderer child in toDo.GetComponentsInChildren<MeshRenderer>())
            child.enabled = toWhat;
        foreach (SkinnedMeshRenderer child in toDo.GetComponentsInChildren<SkinnedMeshRenderer>())
            child.enabled = toWhat;
    }
    // copied from main-- maybe move to utility script?
    public static void hideObjectChildren(GameObject toHide)
    {
        setRenderStateForObject(toHide, false);
    }

    public static void showObjectChildren(GameObject toShow)
    {
        setRenderStateForObject(toShow, true);
    }
}
