# Live Trained Audio Autoencoder
### Overview

The “Live-Trained Audio Autoencoder” employs a custom variational audio autoencoder that is simple enough to be trained very quickly (within minutes) on tiny amounts of audio material (seconds of audio). This allows the autoencoder to generate audio in real time while being trained simultaneously. This opens up the possibility of making the training process of the audio autoencoder a central interactive element in a musical performance. In this scenario, a performer can use the autoencoder as a digital musical instrument whose acoustic characteristics continuously change in direct response to manipulation of the training process.

The main possibilities for manipulating the training process include:

- Manipulating the training set by adding and removing audio files or incorporating live input from a microphone.

- Manipulating the overall training settings that affect how quickly the autoencoder learns and forgets.

- Manipulating which loss functions are employed and how strongly they are weighted during the learning process.


The autoencoder is currently implemented only in Python and is still in its early prototyping stage, both in terms of functionality and user friendliness. However, it is sufficiently usable and stable to allow composers and musicians to experiment with it and provide feedback. This feedback will guide its further development. The long-term goal is to implement and release the autoencoder as a software component that can easily be integrated into popular programming environments for computer music, such as Max/MSP and SuperCollider.

---

### Repository Structure

The repository content is as follows

- The Data/audio folder contains a small set of example audio files can be used a starting point for training the autoencoder. 
- The Data/configs folder contains an example configuration for a user interface.
- The Data/sessions folder contains example logs of previous training and interface manipulation sessions that can be replayed.
- The Docs folder contains instructions for installing the necessary environment for running the autoencoder and a description of the user interface.
- The Installers folders contains project files and scripts for preparing the installation.
- The Software/Autoencoder folder contains the source code for the autoencoder and convenience scripts for running it.

---

