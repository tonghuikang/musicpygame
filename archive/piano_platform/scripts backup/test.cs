using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using IronPython.Hosting;
using IronPython.Modules;
using Microsoft.Scripting.Hosting;


public class test : MonoBehaviour {

    public static ScriptEngine engine = Python.CreateEngine();
    ScriptSource source = engine.CreateScriptSourceFromFile("test.py");
    ScriptScope scope = engine.CreateScope();
    int result_1;
    string result_2;

    // Use this for initialization
    void Start () {

    }

    // Update is called once per frame
    void Update () {
        source.Execute(scope);
        dynamic Calculator = scope.GetVariable("Calculator");
        dynamic calc = Calculator();
        result_1 = calc.add();
        string str = result_1.ToString();
        Debug.Log(str);
        
	}
}


