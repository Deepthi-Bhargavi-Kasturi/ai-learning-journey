# Engineering Journal

## Day 3: Tokenization

Text can't be fed to a model directly — tokenization is the first step,
breaking text into smaller units (tokens): words, subwords, punctuation,
or characters.

Each model has a fixed vocabulary list (all tokens its algorithm can
produce), built from the training data *before* training starts, with a
fixed size limit (e.g. 50k tokens).

Flow: input text → split into tokens → each token mapped to a unique
integer ID (via vocabulary lookup) → ID array fed into the embedding layer.

**Key point:** the integer IDs themselves carry no meaning or relationship
— they're just index lookups. Actual meaning/context is derived later, by
the embedding layer.

## Day 2: How Transformers Solve Tasks (short session)

Light day due to work, but started a new section on how transformer-based
models actually solve tasks under the hood.

Core idea: every model follows the same general pattern — input → process
→ output. What differs between tasks/models is (1) how data is prepared,
(2) which transformer architecture variant is used, and (3) how output is
generated.

Language models are a *subset* of transformer models, trained to predict
the probability of a word given its surrounding context (via CLM or MLM,
covered Day 1).

Three architecture types exist — encoder-only, decoder-only, encoder-decoder
— and the right one depends on the task. E.g., decoder-only (GPT) fits text
generation. Understanding *why* a given architecture suits a given task is
the real goal here, not just memorizing which model uses which.

## Day 1: Transfer Learning & Transformer Architecture

### Transfer Learning vs. Pretraining
- Pretraining: base model trained from scratch, random initial weights,
  massive datasets, huge compute/energy cost.
- Transfer learning / fine-tuning: start from a pretrained model (already
  has statistical/linguistic understanding), then train further on a
  smaller, task-specific dataset. Much lower compute cost, can often
  be done on a single GPU.
- Rule of thumb: the pretrained model you choose should be reasonably
  close in domain/language to your target task.

### Model "Head" vs. "Body"
- Body: the backbone — does the actual pattern analysis, statistical
  understanding of language. This is what gets reused from the
  pretrained model.
- Head: the task-specific output layer (classification/prediction layer).
  Swapped out and retrained for your specific task.

### Architecture vs. Checkpoint
- Architecture = the skeleton/blueprint (e.g. BERT — defines components,
  operations, how they connect).
- Checkpoint = a specific set of trained weights for that architecture
  (e.g. bert-base-cased — the actual saved model).

### Training Objectives
- Causal Language Modeling (CLM): predicts the next word, one direction
  only. Used for text generation. Example: GPT-2.
- Masked Language Modeling (MLM): given a sentence with a word masked
  out, predicts the missing word using context from both sides.
  Example: BERT.

### Transformer Architecture: Encoder vs. Decoder
- Encoder: converts input text into vector embeddings (mathematical
  representation capturing grammar, word relationships, meaning).
  Bidirectional — reads the full sentence left-to-right and right-to-left.
  Uses self-attention (relating words within the same sentence).
- Decoder: generates output one word at a time (autoregressive).
  Unidirectional — can only see words it has already generated, not
  future ones. Uses masked self-attention (future tokens hidden).

### How Encoder + Decoder Work Together (translation example)
- Encoder takes the source sentence (e.g. English) → outputs embeddings
  representing its meaning.
- Decoder receives two separate inputs:
  1. Its own target sequence so far (e.g. Japanese, shifted right with
     a start token) → goes into masked self-attention.
  2. The encoder's output (source sentence meaning) → goes into a
     separate cross-attention layer.
- At step 1, the decoder has no prior generated words yet, but it does
  have full access to the encoder's output via cross-attention — so
  the first word is predicted mainly from the source sentence meaning,
  not from the start token itself (the start token is just a
  positional/structural marker, not a meaningful word).
- From step 2 onward, the decoder also conditions on its own
  previously generated words.

### Attention
- Tells the model how much weight/focus to give each word relative to
  every other word, to build context.
- Example: translating "you like this course" into German — the
  translation of "you," "like" depends on grammatical gender/formality
  rules, but "course" itself may be largely irrelevant to that specific
  word's translation. Attention lets the model focus only on what's
  relevant for each prediction.

### Encoder-only vs. Decoder-only Models
- Encoder-only (BERT): reads full sentence both directions, good for
  understanding tasks like sentiment analysis — output space is fixed
  (e.g. positive/negative), no generation involved.
- Decoder-only (GPT/ChatGPT): autoregressive, generates one token at a
  time based on the prompt + its own previous outputs, never knows the
  next word in advance.

## 📅 Date 

2026-07-06

## 📚 Topic
Transfer Learning & Fine-Tuning

## 💡 What I Learned

Today I learned why modern AI models are usually **fine-tuned** instead of being trained from scratch.

A base model starts with random weights and requires massive datasets, significant compute resources, and weeks (or even months) of training. Fine-tuning, on the other hand, starts with a **pre-trained model** that has already learned language patterns, grammar, and statistical relationships from large datasets.

Because of this prior knowledge:
- Less task-specific data is required.
- Training is much faster.
- Compute requirements are lower (often a single GPU is sufficient).
- The environmental impact is significantly lower than training a model from scratch.

## 🔍 Key Concepts

- Base Model
- Pre-trained Model
- Transfer Learning
- Fine-Tuning
- Weights
- Self-Supervised Learning
- Causal Language Modeling
- Masked Language Modeling

## ✨ Interesting Insights

- Fine-tuning initializes a model with **pre-trained weights** instead of random weights.
- Pre-trained models can transfer their learned language understanding to new tasks.
- Biases present in the original training data can also be transferred.
- Fine-tuning usually improves performance for a specific task compared to using the base pre-trained model directly.
- GPT models are trained using **causal language modeling** (predict the next token).
- BERT is trained using **masked language modeling** (predict missing tokens).

## 🌱 Sustainability Note

Fine-tuning is more sustainable because it reuses an existing model instead of training one from scratch, reducing compute, energy consumption, and training time.

## 🤔 Questions

- What exactly happens to the Transformer body during fine-tuning?
- Which layers are frozen and which are updated?
- Why is only the task-specific head replaced?

## 🚀 Next Step

Understand the architecture of a Transformer model, specifically the **body** and **head**, and how they are used during fine-tuning.
