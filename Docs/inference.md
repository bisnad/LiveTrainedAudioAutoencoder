# Live inference

Listening to the autoencoder while it trains, including live microphone input.

## Output device

The loudspeakers or headphones used for live playback of the autoencoder output.

Changing the device while audio is playing restarts the output stream.

## Source

The audio that is fed through the autoencoder (encoded to a compact code, then decoded back) for live listening: a whole audio file, or 'Live microphone input' to encode your microphone in real time.

File playback always uses the whole source file, even when it is split into several training segments. The listening model is a copy of the training model that is refreshed regularly, so what you hear follows training with a short delay. The microphone input only uses that listening copy and has no effect on training. Use headphones to avoid feedback.

## Source start

Start (seconds) of the section of the source file that is played in a loop. Not used for the microphone.

Together with 'Source end' this selects the loop region. It has no influence on training.

## Source end

End (seconds) of the looped section of the source file.

See 'Source start'.

## Use latent mean

The encoder describes each sound as a probability distribution (a mean and a spread). Normally a random sample is drawn from it; with this option the mean is used instead, so the output is deterministic.

Using the mean usually sounds cleaner and more stable, while sampling shows how much variation the model has learned. The training itself always uses sampling.

## Latent noise

Extra random noise added to the code before decoding. 0 = none.

Larger values make the output increasingly different from the input and eventually unstable. It is useful as a creative control; it never affects training.

## Gain

Output volume factor. 1.0 = unchanged.

A soft limiter keeps loud peaks from clipping, but very high gain will still distort.

## Audio output

Starts and stops the live playback.

Stopping audio also releases the microphone if it is in use.

## Safety buffer (microphone)

How many generated chunks are collected before microphone playback starts. More = fewer dropouts but more delay. 0 = none.

Each chunk is one inference step long. Lower this together with the output latency to reduce delay; if the sound starts to crackle or the underrun counter rises, raise it again.

## Max backlog before skipping ahead

If the model falls this many steps behind the microphone, it skips ahead to the newest audio instead of letting the delay grow.

Smaller values cap the delay at the price of occasional skips when the computer cannot keep up.

## Vocos look-ahead

How many spectrogram frames at the end are held back before playing, because the vocoder needs some future context to render a frame properly. More = better quality, more delay.

Values below the receptive field of Vocos (roughly 27 frames) tend to cause artifacts at the edge. Each frame costs about one hop length of delay.

## Output stream latency

The buffer size requested from the sound card, in milliseconds. Smaller = less delay, higher risk of crackling.

Changing it restarts the output stream after a short pause.

## Microphone block size

How many samples the microphone driver delivers at a time. 0 = driver default. Smaller blocks reduce delay but need more CPU.

Typical low-delay values are 128 to 512 samples.
