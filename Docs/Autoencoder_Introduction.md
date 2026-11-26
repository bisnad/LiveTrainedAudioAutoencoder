# ALTA - Audio Live-Trained Autoencoder
## A Short Introduction to Autoencoders

### What Is an Autoencoder?

An autoencoder is a machine-learning model that learns to convert data, in our case audio, into a highly compressed representation called a latent code. It then reconstructs the original data from that code as faithfully as possible. 

### How Training Works

Like every machine-learning model, an autoencoder must learn from examples before it can perform its task. This learning process is called training, and the data used for it is called the training set. Training repeats the following cycle:

1. Several short audio excerpts from the training set are passed through the model.
2. The model's output (the reconstructed audio) is compared with the original audio.
3. The difference between the original and reconstructed audio is the error. The error is measured by one or several loss functions.
4. The model's internal parameters, called weights, are adjusted slightly so that the error becomes smaller.

This cycle is repeated many times until the error is small enough to be acceptable. Training is then usually stopped, and the model is applied to the task it was trained for, with its weights no longer changing. This use of a trained model is called inference.

### The Model Used in ALTA

The autoencoder in this tool does not work on the audio waveform directly. It works on mel spectrograms, which show how the energy of a sound is distributed over time and over frequency, with a frequency axis that approximates human pitch perception. The autoencoder has two parts:

- The encoder takes a mel spectrogram and produces a latent code.
- The decoder takes a latent code and produces a mel spectrogram.

Only the encoder and the decoder are trained. Computing a mel spectrogram from audio is standard signal processing. Converting a mel spectrogram back into audio is done by a second, separate neural network named Vocos, which has been pre-trained and is used unchanged.

### What Makes ALTA "Live Trained"

Two properties distinguish this application from conventional machine-learning workflows. First, the model is relatively small and can learn from very little material, seconds to minutes of audio, where hours would normally be needed. Second, it trains so quickly, in minutes instead of hours or days, that you can hear the model improve while it is training. The model you hear is a copy of the model being trained, whose weights are updated at regular intervals. Training and inference therefore run simultaneously, instead of the usual sequence of training first and using the model afterwards. This is why the tool is called a live trained autoencoder.

Because the model learns from so little material, what it learns is strongly shaped by your training set. To use the tool fully, it helps to know a few core concepts of machine learning. The glossary below explains the terms that appear in the graphical user interface.

---

## Glossary of Terms

**Training set**: All audio material (audio files and microphone recordings) used to train the model. In the tool, these are the entries in the Audio files list in the Data selection tab whose checkbox is ticked.

**Inference**: Apply the model to audio without changing its weights. The audio is passed into the autoencoder, compressed into latent codes, and decompressed into reconstructed audio, which you can hear in real time. The audio used for inference does not have to be the same audio used for training. Using different audio can lead to interesting timbre transfer effects, in which acoustic characteristics of the training material appear in the inference audio.

**Latent**: The latent code is the compressed representation of the audio used by the autoencoder. It cannot be listened to directly and must be decoded first. In a well-trained model, decoding gives a close (but not exact) reconstruction of the encoded audio. If random noise is added to the latent code before decoding, the reconstructed audio changes, and the more noise is added, the larger the difference from the original. This is one way to generate novel audio. 

**Loss functions**: A loss function calculates the error of the model, which training then tries to reduce. Most loss functions compare the original audio with the reconstructed audio with respect to a specific audio feature, such as spectral shape, loudness, brightness or pitch. Each loss function has a weight, and a weight of 0 switches it off. When several are active, their weighted sum is minimised. Some loss functions mainly improve audio reconstruction fidelity, while others act as audio effects, because the model is pushed to match certain audio features more strictly than others.

**Reconstruction loss**: The total loss used in training has two parts. The first part is the reconstruction loss ("Rec loss" in the interface). The second part is the KL-divergence loss (further explained in this glossary). The reconstruction loss measures how closely the reconstructed audio matches the original, and it is the weighted sum of all the loss functions with a weighting factor bigger than zero. The overall  influence of the reconstruction loss on training is set by the "Rec loss scale".

**KL-divergence loss**: This loss measures how well the latent codes (i.e. the compressed audio representation) are distributed, where a good distribution resembles a Gaussian distribution (a distribution in which the latent codes cluster together at a center and gradually become less dense further away from the center). Nearby latent codes then decode to similar sounds, and there are fewer gaps that decode to implausible audio. Its influence is set by "Beta (KL factor)". A high beta reduces the quality of the reconstruction. Moderate to high values can still give interesting results with timbre transfer and latent noise.

**Learning rate**: The learning rate sets the size of each weight adjustment. A large rate makes learning fast but less accurate. A small rate learns more slowly but can capture finer audio detail. Training often starts with a larger rate and ends with a lower rate. A very large rate makes training unstable, and the audio output can turn into loud noise, so reduce your playback volume before experimenting with it.

**Batch size**: The number of audio excerpts processed together in one training step. Larger batches result in more reliable training, but each trained step requires more computation. The maximum useful value depends on your computer. If the audio output starts to stutter, reduce the batch size.
Weight decay: At every training step, the weights gradually shrink toward zero. The high decay value makes the model forget earlier material and adapt faster to new material. 

**Layers**: A neural network is organised into layers of artificial neurons. Each layer is connected to the previous and the next layer, and data passes through them one after another. In this tool, the "Model reset" controls can re-randomise the weights of the whole model, of the encoder only, of the decoder only, or of a single layer. The "Randomization level" sets how strongly the weights are replaced. Partial resets make the model forget only part of what it has learned.
