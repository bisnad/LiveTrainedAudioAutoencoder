"""
Help popups for the live audio autoencoder GUI.

Every parameter control gets a small "?" button.  Clicking it opens a short, plain-language description and a link
to a longer explanation in a Markdown file in the Docs folder two directories above this script
(<script folder>/../../Docs).  The link is opened in the default web browser.

All texts live in this file.  After editing them, run
    python gui_help.py
to rewrite the Markdown files in the Docs folder from the same texts (existing files are overwritten).
"""
import html
import os
import re
import webbrowser
from pathlib import Path

HERE = os.path.dirname(os.path.abspath(__file__))
DOCS_DIR = os.path.abspath(os.path.join(HERE, "..", "..", "Docs"))

DOC_TITLES = {
    "data": ("Data selection", "Audio files, training segments and microphone recording."),
    "inference": ("Live inference", "Listening to the autoencoder while it trains, including live microphone input."),
    "training": ("Live training", "Optimizer, loss balance, forgetting, adaptation and model reset."),
    "losses": ("Loss functions", "What each loss term compares and what its parameters do."),
    "log": ("Log and session recording", "Loss timeline, experiment logging and replay."),
}

# uid -> (title, short description, longer explanation for the Docs file)
HELP = {
    # ------------------------------------------------------------------ data
    "data.files": ("Audio files",
        "The list of audio files the autoencoder can be trained on. Tick a file to include it in the training set; "
        "unticked audio files are not used for training but can still be listened to in live inference. Long files can optionally be cut into "
        "numbered segments (_1, _2, ...) that can be ticked and trained on independently.",
        "Newly added audio files are never used for training until you tick it. During training, short audio windows are drawn at random "
        "from the ticked audio files, with longer audio files more selected more often than shorter ones. Splitting an audio file only changes the "
        "training list: live inference always plays the whole source file. 'Remove audio files...' deletes audio files "
        "from this list (not from disk); a audio file is unloaded when none of its segments remain."),
    "data.chunk_on_load": ("Duration of segments created from new audio files",
        "Length in seconds of the segments a newly added audio file is cut into for training. 0 keeps the file whole.",
        "Cutting a long recording into segments lets you tick only the parts you want the model to learn, for "
        "example just a particularly interesting passage. Shorter segments do not change how audio is played back."),
    "data.range_start": ("Selected audio file: start",
        "Start time (seconds) of the selected audio file.",
        "These two fields do not cut or trim the entry. Only the width (end minus start) is used when you press "
        "'Split selected into _1, _2, ...'; the whole audio file is divided into segments of that width."),
    "data.range_end": ("Selected audio file: end",
        "End time (seconds) of the selected audio file.",
        "See 'Selected entry: start'."),
    "data.mic_device_panel": ("Audio input device",
        "A microphone or other audio input device used for recording new audio material into the dataset or for providing live "
        "audio input for inference.",
        "The list of audio devices is read once when the program starts, so connect a microphone before launching the application. "
        "The audio input device is locked while a recording is running; a change during live microphone playback takes effect "
        "after you stop and start audio."),
    "data.mic_record_panel": ("Microphone recording",
        "Records from the selected audio input device. The 'Stop and add to dataset' button saves the audio recording as wav file in the data/audio folder and adds "
        "it to the audio files list.",
        "Recordings are limited to a maximum duration of 10 minutes. They are stored at the device's native sample rate and resampled to "
        "48 kHz when loaded."),
    "session.panel": ("Experiment session logging",
        "Records what you change (parameters, files, bookmarks) and training metrics to a new folder so an "
        "experiment can be reviewed or replayed later.",
        "Logging is off by default. No audio and no model weights are copied into the log; only events and sparse "
        "metrics are written."),
    "replay.panel": ("Replay a recorded experiment",
        "Plays back a recorded session by re-applying your logged actions in the GUI, optionally with audio.",
        "Replay re-applies parameter changes, file ticks, splits and playback actions. It cannot restore model "
        "weights from before a reset."),
    # ------------------------------------------------------------------ inference
    "inference.device": ("Audio output device",
        "The loudspeakers or headphones used for live playback of the autoencoder output.",
        "Changing the device while audio is playing restarts the output stream."),
    "inference.file": ("Source Audio",
        "The source audio that is fed through the autoencoder (encoded to a latent code, then decoded back) for live "
        "listening: the source can be an audio file, or 'Live microphone input'.",
        "File playback always uses the whole audio file, even when it is split into several training segments. "
        "The inference model is a copy of the training model that is refreshed regularly, so what you hear follows "
        "training with a short delay. The microphone input only uses that listening copy and has no effect on "
        "training."),
    "inference.start": ("Source audio start",
        "Start (seconds) of the audio source file that is played in a loop. Not used for the microphone.",
        "Together with 'Source audio end' this selects the loop region."),
    "inference.end": ("Source audio end",
        "End (seconds) of the audio source file that is played in a loop. Not used for the microphone.",
        "Together with 'Source audio start' this selects the loop region."),
    "inference.use_mean": ("Use latent mean",
        "The encoder describes each latent code as a normal distribution. Normally a random "
        "sample is drawn from it; with this option the mean of the normal distribution is used instead, so the generated audio is deterministic. "
        "Using the mean usually causes the generated audio to sound cleaner and more stable, while sampling shows how much variation the model "
        "has learned.",
        "The training itself always uses sampling."),
    "inference.noise": ("Latent noise",
        "Extra random noise added to the latent code before decoding. 0 = none. "
        "Larger values make the audio output increasingly different from the audio input and eventually unstable.",
        "It is useful as a creative control; it never affects training."),
    "inference.gain": ("Gain",
        "Audio output volume factor. 1.0 = unchanged.",
        "A soft limiter keeps loud peaks from clipping, but very high gain will still distort."),
    "inference.audio_buttons": ("Audio output",
        "Starts and stops audio playback.", "Stopping audio also releases the microphone if it is in use."),
    "inference.mic_prebuffer": ("Audio buffer queue size (microphone)",
        "How many recorded audio buffers are collected before audio playback starts. More = fewer dropouts but "
        "more delay. 0 = none.",
        "Each audio buffer is one inference step long. Lower this together with the output latency to reduce delay; if "
        "the sound starts to crackle or the underrun counter rises, raise it again."),
    "inference.mic_max_lag": ("Max audio buffer backlog",
        "If the model falls this many steps behind the microphone input, it skips ahead to the newest audio buffer instead of "
        "letting the delay grow.",
        "Smaller values cap the delay at the price of occasional skips when the computer cannot keep up."),
    "inference.lookahead": ("Vocos spectrogram buffer",
        "How many spectrogram frames at the end are held back before playing, because the vocoder needs some "
        "future context to render a audio buffer properly. More = better quality, more delay.",
        "Values below the receptive field of Vocos (roughly 27 frames) tend to cause artifacts at the edge. "
        "Each frame costs about one hop length of delay."),
    "inference.out_latency": ("Output audio buffer size",
        "The audio buffer size requested from the sound card, in milliseconds. Smaller = less delay, higher risk of "
        "crackling.", "Changing it restarts the output stream after a short pause."),
    "inference.mic_input_block": ("Input audio buffer size",
        "How many audio samples the microphone driver delivers at a time. 0 = driver default. Smaller blocks reduce "
        "delay but need more CPU.", "Typical low-delay values are 128 to 512 samples."),
    # ------------------------------------------------------------------ training
    "training.rec_loss_scale": ("Rec loss scale",
        "Multiplies the whole reconstruction part of the loss (all weighted loss terms together) before it is "
        "added to the KL term. It sets how important accurate reconstruction is compared with a well-organised "
        "latent space.",
        "Total loss = rec loss scale x sum(weight x loss) + beta x KL. With adaptive optimizers such as Adam, "
        "scaling the entire loss changes the balance against KL much more than it changes the step size."),
    "training.beta": ("Beta (KL factor)",
        "How strongly the model is pushed to keep its latent codes close to a simple Gaussian distribution (the "
        "KL term of a variational autoencoder).",
        "Higher beta gives a smoother, more regular code that is easier to sample from but blurrier "
        "reconstructions; lower beta gives sharper reconstructions with a less structured code. "
        "The KL term is controlled only by this setting."),
    "training.learning_rate": ("Learning rate",
        "The size of each weight update. Too high makes training unstable; too low makes it slow.",
        "It is shown on a logarithmic scale. For live training small values are usually safer, because every "
        "step is immediately audible. The learning rate also scales the weight-decay shrink per step."),
    "training.optimizer": ("Optimizer",
        "The algorithm that turns the loss gradient into weight updates. AdamW is a robust default.",
        "AdamW and Adam adapt the step size per weight. SGD with momentum is simpler and needs a carefully "
        "tuned learning rate. RMSprop and Adagrad are other adaptive methods. L-BFGS makes several "
        "refinement iterations per step on a fixed batch; it can converge fast but is slow per step and "
        "ignores weight decay."),
    "training.batch_mode": ("Sampling",
        "How training examples are chosen each step: 'Random windows' draws a few random short audio windows from "
        "the ticked entries; 'Full dataset windows' uses windows covering all ticked entries.",
        "Random windows is cheap and noisy. The full-dataset mode is deterministic but is limited to a maximum "
        "number of windows, so it only suits small datasets."),
    "training.batch_size": ("Random batch size",
        "Number of audio windows used per training step in random mode.",
        "Larger batches give smoother, more reliable updates but each step takes longer. For live training a "
        "moderate size keeps the model responsive."),
    "training.lbfgs_iters": ("L-BFGS internal iterations",
        "How many refinement iterations L-BFGS performs inside one training step.",
        "More iterations extract more from a batch but make each step slower. Only used with the L-BFGS optimizer."),
    "training.lbfgs_history": ("L-BFGS history length",
        "How many past updates L-BFGS remembers to estimate the curvature of the loss.",
        "Longer history gives a better estimate but uses more memory. Only used with L-BFGS."),
    "training.lbfgs_hold": ("L-BFGS reuse random batch",
        "How many steps the same random batch is kept for L-BFGS.",
        "L-BFGS needs a consistent loss to estimate curvature, so the batch is held fixed for a number of steps "
        "instead of being redrawn every step."),
    "training.sync_interval": ("Sync to inference",
        "How often (in training steps) the trained weights are copied into the model used for live listening.",
        "Small values let you hear changes sooner; large values make playback more stable between updates."),
    "training.weight_decay": ("Weight decay (forgetting)",
        "At every step the weights shrink slightly toward zero, so the model gradually forgets old material and "
        "adapts faster to new audio. The label below shows the time constant of this forgetting.",
        "The shrink per step is learning rate x decay. Larger values forget faster but can damage what was "
        "learned. L-BFGS ignores it. Other ways to control forgetting are mixing old and new audio in the "
        "training set, ConvLoRA adapters and partial model reset."),
    "training.train_mode": ("Trainable weights",
        "'Full network' trains all weights. The ConvLoRA modes freeze the original weights and train small "
        "added correction layers instead.",
        "ConvLoRA changes the sound less drastically and forgets less, and can be used to specialise a model "
        "that was first trained in full-network mode. Switching modes merges existing adapters into the base "
        "weights so the output stays the same."),
    "training.lora_rank": ("ConvLoRA rank",
        "The size of the small correction layers. Higher rank = more capacity to adapt, but more parameters.",
        "A rank of a few units to a few dozen is typical."),
    "training.lora_alpha": ("ConvLoRA scaling alpha",
        "Scales how strongly the adapters change the layers (commonly relative to the rank).",
        "Larger values make the adapters' effect stronger for the same learned weights."),
    "training.reset_level": ("Randomization level",
        "How much of the selected weights is replaced by fresh random values when you press 'Reset model'. "
        "0 = nothing changes, 1 = completely random.",
        "Level 1 with 'All layers' is a full reset and restarts the step counter. Partial resets keep the step "
        "counter and clear the optimizer memory of the affected weights only."),
    "training.reset_scope": ("Affected weights (reset)",
        "Which weights the reset touches: everything, only the encoder, only the decoder, or one single layer.",
        "Resetting a single layer or one half of the model is a gentler way to free the network from old habits."),
    "training.reset_mix": ("Mixing (reset)",
        "How old and new random weights are combined. 'Linear blend' fades one into the other; "
        "'Variance-preserving' keeps the overall size of the weights constant.",
        "Linear blend: (1 - level) x old + level x new. Variance-preserving: sqrt(1 - level) x old + "
        "sqrt(level) x new, which avoids weights becoming too small in the middle of the range."),
    "training.controls": ("Pause / reset / checkpoint buttons",
        "Pause or resume training, reset the model, and save or load a checkpoint (weights and settings).",
        "Pausing stops weight updates but live listening continues with the current model."),
    # ------------------------------------------------------------------ log
    "log.window_steps": ("Window width (training steps)",
        "How many of the most recent training steps are shown on the loss timeline.",
        "Use a short window to watch fast changes and a long one to judge overall progress."),
    "log.show_total": ("Show total loss",
        "Also draws the total loss (sum of all weighted terms) in the timeline.", ""),
    "log.log_y": ("Log y-axis",
        "Uses a logarithmic vertical axis, which makes terms of very different sizes comparable.", ""),
    "log.plot": ("Loss timeline",
        "Shows every active loss term as it contributes to the total (rec loss scale x weight x loss; KL = beta x "
        "KL) over the last training steps.",
        "Falling lines mean the model gets better at that aspect. A term that stays high may need a larger "
        "weight, or may conflict with other terms."),
}

# loss key -> (title, short description, longer explanation)
LOSS_INFO = {
    "vae_mel": ("VAE log-mel distance",
        "Compares the log-mel spectrograms (the representation the autoencoder itself works in) of the original "
        "and the reconstruction.", "This is the most direct measure of how well the autoencoder reproduces its "
        "input, with a sound-like (mel) frequency scale."),
    "mr_stft": ("Perceptual multi-resolution mel-STFT",
        "Compares spectrograms of the original and the reconstruction at several time/frequency resolutions on a "
        "mel scale, optionally weighted to match hearing.", "Looking at several resolutions at once penalises "
        "both blurred transients and smeared pitches. Implemented with the auraloss library."),
    "mel_mr": ("Multi-resolution log-mel spectrogram",
        "Log-mel spectrograms at several FFT sizes are compared.", "Complements the main mel loss with "
        "additional time/frequency trade-offs."),
    "lin_mr": ("Multi-resolution log linear spectrogram",
        "Compares log spectrograms with a linear frequency axis at several FFT sizes.", "Unlike the mel-based "
        "losses, high frequencies get as much attention as low ones, which helps keep brightness and detail."),
    "mfcc": ("MFCC",
        "Compares mel-frequency cepstral coefficients, a compact summary of the overall spectral shape (timbre).",
        "Good at matching timbre, indifferent to fine detail."),
    "loudness": ("Loudness",
        "Compares how loud each short frame is, using a hearing-weighted measure.", "Keeps the dynamics of the "
        "reconstruction similar to the original."),
    "flatness": ("Spectral flatness",
        "Compares how noise-like (flat spectrum) versus tonal (peaky spectrum) each frequency band is.",
        "Helps the model keep noisy sounds noisy and tonal sounds tonal."),
    "centroid": ("Spectral centroid",
        "Compares the centre of mass of the spectrum, which corresponds to perceived brightness.", ""),
    "lw_centroid": ("Loudness-weighted spectral centroid",
        "A brightness comparison in which loud frames count more than quiet ones.", ""),
    "temporal": ("Temporal centroid",
        "Compares where the energy lies in time within a window (a sudden attack versus a slow swell).", ""),
    "bandwidth": ("Spectral bandwidth",
        "Compares how widely the spectrum is spread around its centroid.", ""),
    "contrast": ("Spectral contrast",
        "Compares the difference between spectral peaks and valleys in octave bands.", "Related to how "
        "clear or dense the sound is."),
    "rolloff": ("Spectral rolloff (soft)",
        "Compares the frequency below which a chosen fraction of the energy lies; a smooth version that can be "
        "trained with gradients.", ""),
    "onset": ("Onset strength",
        "Compares how quickly the spectrum changes from frame to frame, which highlights note onsets and "
        "transients.", ""),
    "rms": ("RMS",
        "Compares the average energy of short frames.", "Similar to loudness but simpler."),
    "zcr": ("Zero-crossing rate (soft)",
        "Compares how often the waveform crosses zero, a rough indicator of noisiness and high-frequency "
        "content.", "A smooth approximation is used so that it can be trained with gradients."),
    "chroma": ("Chroma STFT",
        "Compares how the energy is distributed over the twelve pitch classes (C, C#, ...), ignoring octave.",
        "Encourages correct musical pitches and harmony."),
    "tonnetz": ("Tonnetz",
        "Compares tonal relationships (fifths, thirds) derived from the chroma features.", ""),
    "poly": ("Poly features (spectral polynomial fit)",
        "Compares polynomial curves fitted to each frame's spectrum, a very coarse description of spectral tilt "
        "and shape.", ""),
}

# loss parameter key -> (title, short description, longer explanation)
PARAM_INFO = {
    "dist": ("Distance",
        "How differences are measured: L1 = absolute difference, L2 = squared difference.",
        "L1 is more forgiving to a few large errors and tends to give sharper results; L2 punishes large errors "
        "heavily."),
    "n_bins": ("Mel bins", "Number of frequency bands on the mel scale.", "More bins resolve finer frequency "
        "detail but cost more computation."),
    "perceptual": ("Perceptual weighting",
        "Emphasises frequency regions the ear is most sensitive to.", ""),
    "n_res": ("Resolutions",
        "How many different FFT sizes (time/frequency trade-offs) are compared.", "Each resolution doubles the "
        "FFT size of the previous one, starting from the smallest FFT size."),
    "min_fft": ("Smallest FFT size",
        "The shortest analysis window (in samples). Small windows resolve timing, large ones resolve pitch.", ""),
    "n_mels": ("Mel bands", "Number of mel-scale frequency bands the spectrum is reduced to.", ""),
    "n_bands": ("Bands",
        "Number of frequency bands the spectrum is grouped into before comparison (octave, log-spaced or pooled "
        "bands, depending on the loss). For the linear spectrogram loss 0 means all bins.", ""),
    "n_mfcc": ("MFCC coefficients", "How many cepstral coefficients are compared. Few = coarse spectral "
        "shape, many = finer detail.", ""),
    "n_fft": ("FFT size",
        "Length of the analysis window in samples. Larger = finer frequency detail, coarser timing.", ""),
    "skip_c0": ("Skip c0", "Ignores the first coefficient, which only carries the overall level.", ""),
    "deltas": ("Also match deltas", "Also compares how the coefficients change over time.", ""),
    "mode": ("Mode", "Which loudness measure is used: a fast A-weighted spectrum estimate or the "
        "(experimental) ITU BS.1770 standard.", ""),
    "db_div": ("dB normalization",
        "Divisor that converts decibel differences into a convenient size. Larger = this term counts less.", ""),
    "log2": ("Compare in log2(Hz)", "Compares frequencies on a musical (octave) scale instead of in Hz.", ""),
    "exponent": ("Weight exponent",
        "How strongly loud frames count more than quiet ones. 0 = all frames equal.", ""),
    "frame": ("Frame (samples)", "Length in samples of the short frames the measure is computed on.", ""),
    "segments": ("Segments per window", "Number of time segments the window is divided into.", ""),
    "sharpness": ("Softness / sharpness",
        "Controls how closely a smooth approximation follows the hard version of the measure. Higher = sharper "
        "but less smooth for training.", ""),
    "percent": ("Energy fraction", "Fraction of the spectrum's energy that lies below the rolloff frequency.", ""),
    "fmin": ("Lowest band edge", "Lowest frequency (Hz) of the first band.", ""),
    "quantile": ("Peak/valley quantile",
        "Which fraction of the strongest and weakest bins counts as peak and valley.", ""),
    "lag": ("Frame lag", "How many frames apart the spectra are compared to detect change.", ""),
    "in_db": ("Compare in dB", "Compare on a decibel scale instead of linear amplitude.", ""),
    "sigma": ("Pitch-class width", "How broadly a frequency is spread over neighbouring semitones.", ""),
    "order": ("Polynomial order", "Degree of the curve fitted to the spectrum; 0 = just the level, 1 = tilt, ...", ""),
    "fit": ("Fit on", "Whether the curve is fitted to the log or the linear magnitude.", ""),
}

_GENERIC = ("No detailed description is available for this control yet.", "")


def slug(title):
    """GitHub-style heading anchor."""
    text = re.sub(r"[^\w\s-]", "", title.lower())
    return re.sub(r"\s+", "-", text.strip())


def _group(uid):
    group = uid.split(".")[0]
    return {"session": "log", "replay": "log"}.get(group, group)


def resolve(uid, label=""):
    """Return dict(title, short, more, doc, anchor, used_in) for a control id."""
    if uid in HELP:
        title, short, more = HELP[uid]
        return dict(title=title, short=short, more=more, doc=_group(uid), anchor=slug(title), used_in="")
    m = re.match(r"losses\.(\w+)\.(\w+)$", uid)
    if m and m.group(1) in LOSS_INFO:
        key, param = m.groups()
        loss_title, loss_short, _ = LOSS_INFO[key]
        if param == "weight":
            return dict(
                title="Loss weights",
                short=f"How strongly the '{loss_title}' term counts in the total loss. 0 switches it off "
                      f"(and saves its computation). {loss_short}",
                more="", doc="losses", anchor=slug("Loss weights"), used_in=loss_title)
        if param in PARAM_INFO:
            title, short, more = PARAM_INFO[param]
            return dict(title=title, short=short, more=more, doc="losses", anchor=slug(title), used_in=loss_title)
    return dict(title=label or uid, short=_GENERIC[0], more=_GENERIC[1], doc=None, anchor="", used_in="")


def doc_path(info):
    return os.path.join(DOCS_DIR, info["doc"] + ".md") if info.get("doc") else None


def doc_uri(info):
    path = doc_path(info)
    if path is None:
        return None
    uri = Path(path).resolve().as_uri()
    return uri + ("#" + info["anchor"] if info.get("anchor") else "")


def open_doc(info):
    uri = doc_uri(info)
    if uri is None:
        return
    try:
        if not webbrowser.open(uri):
            raise RuntimeError("no browser")
    except Exception:
        from PyQt5 import QtCore, QtGui
        QtGui.QDesktopServices.openUrl(QtCore.QUrl(uri))


# ------------------------------------------------------------------------------------------ Qt part
_OPEN = {}


def show_help(anchor_widget, uid, label=""):
    from PyQt5 import QtCore, QtWidgets
    info = resolve(uid, label)
    if uid in _OPEN:
        try:
            _OPEN[uid].raise_()
            _OPEN[uid].activateWindow()
            return
        except RuntimeError:
            _OPEN.pop(uid, None)
    dlg = QtWidgets.QDialog(anchor_widget.window() if anchor_widget is not None else None)
    dlg.setWindowTitle("Help: " + info["title"])
    dlg.setAttribute(QtCore.Qt.WA_DeleteOnClose)
    dlg.setMinimumWidth(420)
    lay = QtWidgets.QVBoxLayout(dlg)
    head = QtWidgets.QLabel(f"<b>{html.escape(info['title'], quote=False)}</b>")
    head.setStyleSheet("font-size: 14px;")
    lay.addWidget(head)
    text = QtWidgets.QLabel(info["short"])
    text.setTextFormat(QtCore.Qt.PlainText)
    text.setWordWrap(True)
    text.setTextInteractionFlags(QtCore.Qt.TextSelectableByMouse)
    lay.addWidget(text)
    if info["used_in"]:
        used = QtWidgets.QLabel(f"<i>Used in: {html.escape(info['used_in'], quote=False)}</i>")
        used.setWordWrap(True)
        lay.addWidget(used)
    path = doc_path(info)
    if path is not None:
        link = QtWidgets.QLabel()
        link.setWordWrap(True)
        if os.path.isfile(path):
            link.setText(f'<a href="doc">More information: {html.escape(os.path.basename(path), quote=False)}</a>')
            link.linkActivated.connect(lambda *_: open_doc(info))
        else:
            link.setText(f"<i>More information: {html.escape(path)} (file not found; run "
                         f"<code>python gui_help.py</code> to create the Docs files)</i>")
        lay.addWidget(link)
    row = QtWidgets.QHBoxLayout()
    row.addStretch(1)
    close = QtWidgets.QPushButton("Close")
    close.clicked.connect(dlg.close)
    row.addWidget(close)
    lay.addLayout(row)
    _OPEN[uid] = dlg
    dlg.destroyed.connect(lambda *_: _OPEN.pop(uid, None))
    dlg.show()


def make_help_button(uid, label=""):
    """A small round '?' button that opens the help popup for control `uid`."""
    from PyQt5 import QtCore, QtWidgets
    btn = QtWidgets.QToolButton()
    btn.setText("?")
    btn.setFixedSize(18, 18)
    btn.setFocusPolicy(QtCore.Qt.NoFocus)
    btn.setCursor(QtCore.Qt.PointingHandCursor)
    btn.setToolTip("info")
    btn.setStyleSheet("QToolButton { border: 1px solid #4a7fc1; border-radius: 9px; color: #4a7fc1; "
                      "font-weight: bold; padding: 0px; } QToolButton:hover { background: #4a7fc1; color: white; }")
    btn.clicked.connect(lambda *_: show_help(btn, uid, label))
    return btn


# ------------------------------------------------------------------------------------------ Docs writer
def _section(title, short, more):
    parts = [f"## {title}", "", short]
    if more:
        parts += ["", more]
    return "\n".join(parts) + "\n"


def write_docs(directory=DOCS_DIR):
    os.makedirs(directory, exist_ok=True)
    pages = {}
    for uid, (title, short, more) in HELP.items():
        pages.setdefault(_group(uid), []).append(_section(title, short, more))
    loss_sections = [_section("Loss weights",
        "Each loss term has a weight. The total reconstruction loss is the sum of weight x loss over all terms, "
        "multiplied by 'Rec loss scale'; the KL term (beta x KL) is added on top. A weight of 0 switches a term "
        "off and saves its computation.", "")]
    for key, (title, short, more) in LOSS_INFO.items():
        loss_sections.append(_section(title, short, more))
    loss_sections.append("# Parameters used by several losses\n")
    for key, (title, short, more) in PARAM_INFO.items():
        loss_sections.append(_section(title, short, more))
    pages["losses"] = loss_sections
    for group, (name, intro) in DOC_TITLES.items():
        body = f"# {name}\n\n{intro}\n\n" + "\n".join(pages.get(group, []))
        with open(os.path.join(directory, group + ".md"), "w", encoding="utf-8") as fh:
            fh.write(body)
    return sorted(os.listdir(directory))


if __name__ == "__main__":
    print("Wrote:", write_docs())
