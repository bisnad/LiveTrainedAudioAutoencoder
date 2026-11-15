# Data selection

Audio files, training segments and microphone recording.

## Audio files (training entries)

The list of audio entries the autoencoder can learn from. Tick an entry to include it in training; unticked entries are ignored by training but can still be listened to. Long files can be cut into numbered segments (_1, _2, ...) that are ticked and trained independently.

Newly added audio is never trained on until you tick it. During training, short windows are drawn at random from the ticked entries, longer entries more often than shorter ones. Splitting a file only changes the training list: live inference always plays the whole source file. 'Remove audio files...' deletes entries from this list (not from disk); a source file is unloaded when none of its segments remain.

## Training segments for new files

Length in seconds of the pieces a newly added file is cut into for training. 0 keeps the file whole.

Cutting a long recording into segments lets you tick only the parts you want the model to learn, for example just a particularly interesting passage. Shorter segments do not change how audio is played back.

## Selected entry: start

Start time (seconds) of the selected entry. Together with 'end' it defines the chunk width used by the Split button.

These two fields do not cut or trim the entry. Only the width (end minus start) is used when you press 'Split selected into _1, _2, ...'; the whole entry is then divided into chunks of that width.

## Selected entry: end

End time (seconds) of the selected entry. The width end minus start is the chunk length used by Split.

See 'Selected entry: start'.

## Audio input device

The microphone or other audio input used for recording new material into the dataset and for the live microphone input in the Live inference tab.

The list of devices is read once when the program starts, so connect a USB microphone before launching. The device is locked while a recording is running; a change during live microphone playback takes effect after you stop and start audio.

## Microphone recording

Records from the selected input device. 'Stop and add to dataset' saves a WAV file in data/audio and adds it to the file list (unticked, so it is not trained on until you tick it).

Recordings are limited to 10 minutes. They are stored at the device's native sample rate and resampled to 48 kHz when loaded.
