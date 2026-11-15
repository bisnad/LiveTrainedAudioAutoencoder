# Live training

Optimizer, loss balance, forgetting, adaptation and model reset.

## Rec loss scale

Multiplies the whole reconstruction part of the loss (all weighted loss terms together) before it is added to the KL term. It sets how important accurate reconstruction is compared with a well-organised latent space.

Total loss = rec loss scale x sum(weight x loss) + beta x KL. With adaptive optimizers such as Adam, scaling the entire loss changes the balance against KL much more than it changes the step size.

## Beta (KL factor)

How strongly the model is pushed to keep its latent codes close to a simple Gaussian distribution (the KL term of a variational autoencoder).

Higher beta gives a smoother, more regular code that is easier to sample from but blurrier reconstructions; lower beta gives sharper reconstructions with a less structured code. The KL term is controlled only by this setting.

## Learning rate

The size of each weight update. Too high makes training unstable; too low makes it slow.

It is shown on a logarithmic scale. For live training small values are usually safer, because every step is immediately audible. The learning rate also scales the weight-decay shrink per step.

## Optimizer

The algorithm that turns the loss gradient into weight updates. AdamW is a robust default.

AdamW and Adam adapt the step size per weight. SGD with momentum is simpler and needs a carefully tuned learning rate. RMSprop and Adagrad are other adaptive methods. L-BFGS makes several refinement iterations per step on a fixed batch; it can converge fast but is slow per step and ignores weight decay.

## Sampling

How training examples are chosen each step: 'Random windows' draws a few random short audio windows from the ticked entries; 'Full dataset windows' uses windows covering all ticked entries.

Random windows is cheap and noisy. The full-dataset mode is deterministic but is limited to a maximum number of windows, so it only suits small datasets.

## Random batch size

Number of audio windows used per training step in random mode.

Larger batches give smoother, more reliable updates but each step takes longer. For live training a moderate size keeps the model responsive.

## L-BFGS internal iterations

How many refinement iterations L-BFGS performs inside one training step.

More iterations extract more from a batch but make each step slower. Only used with the L-BFGS optimizer.

## L-BFGS history length

How many past updates L-BFGS remembers to estimate the curvature of the loss.

Longer history gives a better estimate but uses more memory. Only used with L-BFGS.

## L-BFGS reuse random batch

How many steps the same random batch is kept for L-BFGS.

L-BFGS needs a consistent loss to estimate curvature, so the batch is held fixed for a number of steps instead of being redrawn every step.

## Sync to inference

How often (in training steps) the trained weights are copied into the model used for live listening.

Small values let you hear changes sooner; large values make playback more stable between updates.

## Weight decay (forgetting)

At every step the weights shrink slightly toward zero, so the model gradually forgets old material and adapts faster to new audio. The label below shows the time constant of this forgetting.

The shrink per step is learning rate x decay. Larger values forget faster but can damage what was learned. L-BFGS ignores it. Other ways to control forgetting are mixing old and new audio in the training set, ConvLoRA adapters and partial model reset.

## Trainable weights

'Full network' trains all weights. The ConvLoRA modes freeze the original weights and train small added correction layers instead.

ConvLoRA changes the sound less drastically and forgets less, and can be used to specialise a model that was first trained in full-network mode. Switching modes merges existing adapters into the base weights so the output stays the same.

## ConvLoRA rank

The size of the small correction layers. Higher rank = more capacity to adapt, but more parameters.

A rank of a few units to a few dozen is typical.

## ConvLoRA scaling alpha

Scales how strongly the adapters change the layers (commonly relative to the rank).

Larger values make the adapters' effect stronger for the same learned weights.

## Randomization level

How much of the selected weights is replaced by fresh random values when you press 'Reset model'. 0 = nothing changes, 1 = completely random.

Level 1 with 'All layers' is a full reset and restarts the step counter. Partial resets keep the step counter and clear the optimizer memory of the affected weights only.

## Affected weights (reset)

Which weights the reset touches: everything, only the encoder, only the decoder, or one single layer.

Resetting a single layer or one half of the model is a gentler way to free the network from old habits.

## Mixing (reset)

How old and new random weights are combined. 'Linear blend' fades one into the other; 'Variance-preserving' keeps the overall size of the weights constant.

Linear blend: (1 - level) x old + level x new. Variance-preserving: sqrt(1 - level) x old + sqrt(level) x new, which avoids weights becoming too small in the middle of the range.

## Pause / reset / checkpoint buttons

Pause or resume training, reset the model, and save or load a checkpoint (weights and settings).

Pausing stops weight updates but live listening continues with the current model.
