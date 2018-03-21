   static Complex[] fft(Complex[] audio_clip_array) {
        int clip_length = audio_clip_array.Length;
        if (clip_length <= 1) {
            return audio_clip_array;
        }

        Complex[] pre_odd = new Complex[clip_length / 2];
        Complex[] pre_even = new Complex[clip_length - clip_length / 2];

        for (int i = 0; i <= clip_length; i++){
            if (i % 2 == 0){
                pre_even[i / 2] = audio_clip_array[i];
            }
            else {
                pre_odd[i / 2] = audio_clip_array[i];
            }
        
            Complex[] after_odd = fft(pre_odd);
            Complex[] after_even = fft(pre_even);

            Complex complex_1 = new Complex(0f, -2f);
            Complex[] T = new Complex[clip_length / 2];

            Complex[] final_1 = new Complex[clip_length / 2];
            Complex[] final_2 = new Complex[clip_length / 2];

            for (int k = 0; k < clip_length / 2; k++) {
                Complex complex_2 = complex_1 * Mathf.PI * k / clip_length;
                T[k] = Complex.Exp(complex_2);

                final_1[k] = after_even[k] + T[k];
                final_2[k] = after_even[k] - T[k];
            }

            Complex[] fft_output_2 = new Complex[final_1.Length + final_2.Length];
            final_1.CopyTo(fft_output_2, 0);
            final_2.CopyTo(fft_output_2, final_1.Length);

            return fft_output_2;
            }
        }

