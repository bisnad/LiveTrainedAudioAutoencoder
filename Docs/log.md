# Log and session recording

Loss timeline, experiment logging and replay.

## Experiment session logging

Records what you change (parameters, files, bookmarks) and training metrics to a new folder so an experiment can be reviewed or replayed later.

Logging is off by default. No audio and no model weights are copied into the log; only events and sparse metrics are written.

## Replay a recorded experiment

Plays back a recorded session by re-applying your logged actions in the GUI, optionally with audio.

Replay re-applies parameter changes, file ticks, splits and playback actions. It cannot restore model weights from before a reset.

## Window width (training steps)

How many of the most recent training steps are shown on the loss timeline.

Use a short window to watch fast changes and a long one to judge overall progress.

## Show total loss

Also draws the total loss (sum of all weighted terms) in the timeline.

## Log y-axis

Uses a logarithmic vertical axis, which makes terms of very different sizes comparable.

## Loss timeline

Shows every active loss term as it contributes to the total (rec loss scale x weight x loss; KL = beta x KL) over the last training steps.

Falling lines mean the model gets better at that aspect. A term that stays high may need a larger weight, or may conflict with other terms.
