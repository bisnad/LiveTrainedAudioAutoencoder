# Loss functions

What each loss term compares and what its parameters do.

## Loss weights

Each loss term has a weight. The total reconstruction loss is the sum of weight x loss over all terms, multiplied by 'Rec loss scale'; the KL term (beta x KL) is added on top. A weight of 0 switches a term off and saves its computation.

## VAE log-mel distance

Compares the log-mel spectrograms (the representation the autoencoder itself works in) of the original and the reconstruction.

This is the most direct measure of how well the autoencoder reproduces its input, with a sound-like (mel) frequency scale.

## Perceptual multi-resolution mel-STFT

Compares spectrograms of the original and the reconstruction at several time/frequency resolutions on a mel scale, optionally weighted to match hearing.

Looking at several resolutions at once penalises both blurred transients and smeared pitches. Implemented with the auraloss library.

## Multi-resolution log-mel spectrogram

Log-mel spectrograms at several FFT sizes are compared.

Complements the main mel loss with additional time/frequency trade-offs.

## Multi-resolution log linear spectrogram

Compares log spectrograms with a linear frequency axis at several FFT sizes.

Unlike the mel-based losses, high frequencies get as much attention as low ones, which helps keep brightness and detail.

## MFCC

Compares mel-frequency cepstral coefficients, a compact summary of the overall spectral shape (timbre).

Good at matching timbre, indifferent to fine detail.

## Loudness

Compares how loud each short frame is, using a hearing-weighted measure.

Keeps the dynamics of the reconstruction similar to the original.

## Spectral flatness

Compares how noise-like (flat spectrum) versus tonal (peaky spectrum) each frequency band is.

Helps the model keep noisy sounds noisy and tonal sounds tonal.

## Spectral centroid

Compares the centre of mass of the spectrum, which corresponds to perceived brightness.

## Loudness-weighted spectral centroid

A brightness comparison in which loud frames count more than quiet ones.

## Temporal centroid

Compares where the energy lies in time within a window (a sudden attack versus a slow swell).

## Spectral bandwidth

Compares how widely the spectrum is spread around its centroid.

## Spectral contrast

Compares the difference between spectral peaks and valleys in octave bands.

Related to how clear or dense the sound is.

## Spectral rolloff (soft)

Compares the frequency below which a chosen fraction of the energy lies; a smooth version that can be trained with gradients.

## Onset strength

Compares how quickly the spectrum changes from frame to frame, which highlights note onsets and transients.

## RMS

Compares the average energy of short frames.

Similar to loudness but simpler.

## Zero-crossing rate (soft)

Compares how often the waveform crosses zero, a rough indicator of noisiness and high-frequency content.

A smooth approximation is used so that it can be trained with gradients.

## Chroma STFT

Compares how the energy is distributed over the twelve pitch classes (C, C#, ...), ignoring octave.

Encourages correct musical pitches and harmony.

## Tonnetz

Compares tonal relationships (fifths, thirds) derived from the chroma features.

## Poly features (spectral polynomial fit)

Compares polynomial curves fitted to each frame's spectrum, a very coarse description of spectral tilt and shape.

# Parameters used by several losses

## Distance

How differences are measured: L1 = absolute difference, L2 = squared difference.

L1 is more forgiving to a few large errors and tends to give sharper results; L2 punishes large errors heavily.

## Mel bins

Number of frequency bands on the mel scale.

More bins resolve finer frequency detail but cost more computation.

## Perceptual weighting

Emphasises frequency regions the ear is most sensitive to.

## Resolutions

How many different FFT sizes (time/frequency trade-offs) are compared.

Each resolution doubles the FFT size of the previous one, starting from the smallest FFT size.

## Smallest FFT size

The shortest analysis window (in samples). Small windows resolve timing, large ones resolve pitch.

## Mel bands

Number of mel-scale frequency bands the spectrum is reduced to.

## Bands

Number of frequency bands the spectrum is grouped into before comparison (octave, log-spaced or pooled bands, depending on the loss). For the linear spectrogram loss 0 means all bins.

## MFCC coefficients

How many cepstral coefficients are compared. Few = coarse spectral shape, many = finer detail.

## FFT size

Length of the analysis window in samples. Larger = finer frequency detail, coarser timing.

## Skip c0

Ignores the first coefficient, which only carries the overall level.

## Also match deltas

Also compares how the coefficients change over time.

## Mode

Which loudness measure is used: a fast A-weighted spectrum estimate or the (experimental) ITU BS.1770 standard.

## dB normalization

Divisor that converts decibel differences into a convenient size. Larger = this term counts less.

## Compare in log2(Hz)

Compares frequencies on a musical (octave) scale instead of in Hz.

## Weight exponent

How strongly loud frames count more than quiet ones. 0 = all frames equal.

## Frame (samples)

Length in samples of the short frames the measure is computed on.

## Segments per window

Number of time segments the window is divided into.

## Softness / sharpness

Controls how closely a smooth approximation follows the hard version of the measure. Higher = sharper but less smooth for training.

## Energy fraction

Fraction of the spectrum's energy that lies below the rolloff frequency.

## Lowest band edge

Lowest frequency (Hz) of the first band.

## Peak/valley quantile

Which fraction of the strongest and weakest bins counts as peak and valley.

## Frame lag

How many frames apart the spectra are compared to detect change.

## Compare in dB

Compare on a decibel scale instead of linear amplitude.

## Pitch-class width

How broadly a frequency is spread over neighbouring semitones.

## Polynomial order

Degree of the curve fitted to the spectrum; 0 = just the level, 1 = tilt, ...

## Fit on

Whether the curve is fitted to the log or the linear magnitude.
