using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using IronPython.Hosting;
using IronPython.Modules;
using Microsoft.Scripting.Hosting;
using System.Numerics;

[RequireComponent (typeof (AudioSource))]
public class AudioPeer : MonoBehaviour {

    // setting up Python environment
    public static ScriptEngine engine = Python.CreateEngine();
    ScriptSource source = engine.CreateScriptSourceFromFile("cqt_class_updated.py");
    ScriptScope scope = engine.CreateScope();

    //setting up Microphone environment
    public AudioSource Aud;
    public AudioClip AudClip;
    public bool UseMic;
    public string SelectedDevice;
    public float[] Samples = new float[512];

    public static float Amplitude, AmplitudeBuffer;
    float AmplitudeHighest;

    //call kernels database
    Complex[,] fft_kernels = kernels.kernels();

    void Start () {
        Aud = GetComponent<AudioSource>();
       
        if (UseMic) {
            if (Microphone.devices.Length > 0)
            {
                SelectedDevice = Microphone.devices[0].ToString();
                Aud.clip = Microphone.Start(SelectedDevice, true, 1, AudioSettings.outputSampleRate);
                Aud.loop = true;
            }
            else {
                UseMic = false;
                Debug.Log("No Microphone connected");
            }
        }
        
        if (!UseMic) {
        }
	}
	
	void Update () {
        //GetAmplitude();
        //GetSpectrum();
        JudgeAmplitude();
        JudgeNote();
        Test();
   
    }

    void Test() {
   
    }

    void JudgeNote() {
        float[] Audioclip = new float[Aud.clip.samples * Aud.clip.channels];
        Aud.clip.GetData(Audioclip, 0);
        source.Execute(scope);
        dynamic Note_Detect = scope.GetVariable("Example");
        dynamic cqt = Note_Detect();
        // Indicator 
        Debug.Log("Start");
        Debug.Log(Audioclip.Length);

        ICollection<int>Notes = cqt.function(Audioclip);

        // Indicator
        Debug.Log("Pass");

        int count = 0;
        foreach (int Note in Notes) {
            Debug.Log(Note);
            count++;
            Debug.Log(count);
        }
        Aud.clip.SetData(Audioclip, 0);
    }

    void GetAmplitude() {

    }

    void GetSpectrum() {
        Aud.GetSpectrumData(Samples, 0, FFTWindow.Blackman);
    }

    void JudgeAmplitude() {
        float Amplitudes;
        Amplitudes = 0;
        foreach (float element in Samples){
            Amplitudes += element;
        }

        if (Amplitudes > 0.5f)
        {
            AudioClip Sound = Aud.clip;
        }
        else {
            //Debug.Log("Sound is too quiet");
        }
    }

    public static int BitReverse(int n, int bits)
    {
        int reversedN = n;
        int count = bits - 1;

        n >>= 1;
        while (n > 0)
        {
            reversedN = (reversedN << 1) | (n & 1);
            count--;
            n >>= 1;
        }

        return ((reversedN << count) & ((1 << bits) - 1));
    }

    /* Uses Cooley-Tukey iterative in-place algorithm with radix-2 DIT case
     * assumes no of points provided are a power of 2 */
    public static void FFT(Complex[] buffer)
    {

        int bits = (int)Mathf.Log(buffer.Length, 2);
        for (int j = 1; j < buffer.Length / 2; j++)
        {

            int swapPos = BitReverse(j, bits);
            var temp = buffer[j];
            buffer[j] = buffer[swapPos];
            buffer[swapPos] = temp;
        }

        for (int N = 2; N <= buffer.Length; N <<= 1)
        {
            for (int i = 0; i < buffer.Length; i += N)
            {
                for (int k = 0; k < N / 2; k++)
                {

                    int evenIndex = i + k;
                    int oddIndex = i + k + (N / 2);
                    var even = buffer[evenIndex];
                    var odd = buffer[oddIndex];

                    double term = -2 * Mathf.PI * k / (double)N;
                    Complex exp = new Complex(Mathf.Cos((float)term), Mathf.Sin((float)term)) * odd;

                    buffer[evenIndex] = even + exp;
                    buffer[oddIndex] = even - exp;

                }
            }
        }
    }

    static Complex[] Convert(float[] float_array) {
        int count = 0;
        Complex[] complex_array = new Complex[float_array.Length];
        foreach (float num in float_array) {
            Complex complex_num = new Complex(num, 0f);
            complex_array[count] = complex_num;
            count++;
        }
        return complex_array;
    }

    int[] cqt_function(Complex[] signal_to_ayse) {

        int array_len = signal_to_ayse.Length;
        FFT(signal_to_ayse);
        Complex[] freq_domain = signal_to_ayse;


        int bins = 36;
        Complex[] freq_ref_notes = new Complex[bins];
        for (int n = 0; n < bins; n++) {
            float number = (n / 36f + 4f / 72f);
            freq_ref_notes[n] = new Complex(261.625565f * Mathf.Pow(2f, number), 0f);
        }
        Complex[,] cqt_resp_specs = new Complex[36, 4096];
        Complex[] cqt_resp = new Complex[36];


        for (int note = 0; note < 36; note++) {
            Complex[] cqt_resp_spec = new Complex[4096];
            for (int entry = 0; entry < array_len; entry++){
                cqt_resp_spec[entry] = fft_kernels[note, entry] * freq_domain[entry];
                cqt_resp_specs[note, entry] = fft_kernels[note, entry] * freq_domain[entry];
            }

            Complex sum = new Complex(0f, 0f);
            foreach (Complex num in cqt_resp_spec) {
                float num_real = Mathf.Abs((float)num.Real);
                float num_imag = Mathf.Abs((float)num.Imaginary);
                Complex Transition_1 = new Complex(num_real, num_imag);
                sum += Transition_1;
            cqt_resp[note] = sum;
            }
        }


        Complex[] notesrum = cqt_resp;
        Complex[] notesrum_peak_only = new Complex[notesrum.Length];


        for (int index = 1; index < 35; index++) {
            if (notesrum[index - 1].Real < notesrum[index].Real && notesrum[index + 1].Real < notesrum[index].Real) {
                notesrum_peak_only[index] = notesrum[index];
            }
        }


        // known_octave = notesrum_peak_only[:]
        Complex[] known_octave = new Complex[notesrum.Length];
        int count = 0;
        foreach (Complex element in notesrum_peak_only) {
            known_octave[count] = element;
            count++;
        }


        // notesrum_peak_only_sum = sum(notesrum_peak_only)
        Complex notesrum_peak_only_sum = new Complex(0f, 0f);
        foreach (Complex element in notesrum_peak_only) {
            notesrum_peak_only_sum += element;
        }

        for (int x = 0; x < 36; x++) {
            if ((float)known_octave[x].Real / (float)notesrum_peak_only_sum.Real < 0.1) {
                known_octave[x] = 0;
            }
        }

        Complex[] known_octave_notes = new Complex[12];
        for (int notes = 0; notes < 12; notes++) {
            known_octave_notes[notes] = known_octave[3 * notes] + known_octave[3 * notes + 1] + known_octave[3 * notes + 2];
        }

        // notestrum_sum = sum(notesrum)
        Complex notesrum_sum = new Complex(0f, 0f);
        foreach (Complex element in notesrum) {
            notesrum_sum += element;
        }

        var list = new List<int>();

        for (int x = 0; x < 12; x++) {
            if ((float)known_octave_notes[x].Real / (float)notesrum_peak_only_sum.Real > 0.1) {
                list.Add(x + 1);
            }
        }

        int[] output = list.ToArray();
        return output;
    }

    

}
