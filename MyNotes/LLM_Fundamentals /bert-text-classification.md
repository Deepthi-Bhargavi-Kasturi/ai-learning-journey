# Text Classification with BERT

## What is text classification?

Text classification assigns one or more predefined categories/labels to an input text. The input may be a sentence, a review, an email, or a longer text document.

Examples include:

- **Sentiment analysis:** classifying a restaurant review as *positive* or *negative* (sometimes *neutral* is also a label).
- **Spam detection:** classifying an email or message as *spam* or *not spam*.
- **Topic classification:** classifying an article as *sports*, *technology*, *politics*, and so on.

## Where BERT fits

**BERT** stands for **Bidirectional Encoder Representations from Transformers**. It is a Transformer **encoder-only** language model introduced by Google researchers in 2018.

Encoder-only models are commonly used for understanding tasks such as text classification. This is a common choice, not an exclusive rule: other model architectures can also be adapted for classification.

BERT is first **pre-trained** on general text, then **fine-tuned** on labelled examples for a particular task, such as sentiment analysis.

## Bidirectional context and masking

In BERT, for example, to infer a missing word in `Cats are cute and they like to eat [MASK]`, the model can use words both before and after the missing position when they exist.

Without masking, a bidirectional model could indirectly see the target word itself during training and make prediction trivial. BERT avoids this with **masked language modelling (MLM)**:

1. It selects 15% of WordPiece token positions for prediction.
2. Of those selected positions:
   - 80% are replaced with `[MASK]`.
   - 10% are replaced with a random vocabulary token.
   - 10% are left unchanged.
3. The model predicts the original token only at the selected positions.

The `80% / 10% / 10%` split applies to the selected 15% of tokens, not to all input tokens.

## Tokenization

The original BERT uses **WordPiece tokenization**. Rather than always treating a whole word as one unit, WordPiece can split a word into smaller subword tokens. For example, a word may be represented as `play` and `##ing`.

This helps a model handle rare or unseen words by composing them from familiar pieces.

## BERT input format

For a single text or a pair of text segments, BERT uses special tokens such as:

```text
[CLS] sentence A [SEP] sentence B [SEP]
```

- **`[CLS]` (classification token):** placed at the beginning of every input sequence. Its final hidden state can learn to represent information useful for classifying the whole input and is commonly used as an aggregate representation for sequence-level classification.
- **`[SEP]` (separator token):** marks boundaries between segments and the end of the input sequence. It is used even when the input contains only one segment.
- **Segment (token-type) embeddings:** learned vectors added to tokens to distinguish segment A from segment B in the original BERT setup.
- **Position embeddings:** learned vectors that provide each token's position in the sequence. They are also part of BERT's input representation.
- **sequence-level classification:** assigning one label to the entire input sequence, not to individual token.

For every token, BERT adds together its token embedding, segment embedding, and position embedding.

The final hidden state is the input to the classification head.

## Segment embeddings

When BERT receives two segments, it adds one learned segment embedding (`E_A`) to tokens in the first segment and another (`E_B`) to tokens in the second segment. These embeddings tell the model which segment each token belongs to.

In the original BERT, “sentence” can mean an arbitrary contiguous span of text, not necessarily a grammatical sentence.

## Pre-training objectives

The original BERT paper used two pre-training objectives.

### 1. Masked language modelling (MLM)

Some input tokens are selected and corrupted as described above. The final hidden state at each selected position (Masked Tokens) is passed through a prediction layer (feed-forward Neural Network) and a softmax over the vocabulary. The model is trained to assign high probability to the original token.

MLM teaches BERT contextual language representations. It is **not** text classification training; text classification is normally a downstream task performed during fine-tuning.

### 2. Next sentence prediction (NSP)

For the original BERT, a pair of segments was labelled as either:

- **IsNext:** segment B really followed segment A in the source text.
- **NotNext:** segment B was a random segment from the corpus.

NSP was part of the original BERT pre-training recipe. Later BERT-family models may omit or replace NSP, so it should not be assumed to apply to every BERT-like model.

## Hidden states

A **hidden state** is an internal vector representation produced for a token at a particular Transformer layer. It **encodes** the token together with the context that the model has incorporated so far.

The final Transformer layer produces a **final hidden state for every input token**, including `[CLS]` and `[MASK]`. It does not produce one single final hidden state for the entire text. Instead:

- For MLM, the final hidden state at a selected token position is used to predict that position's original token.
- For sequence classification, the final hidden state for `[CLS]` is commonly passed to a classification head.

In the example `Cats are cute and they like to eat [MASK]`, the final hidden state at `[MASK]` contains contextual information from the surrounding tokens. The prediction layer uses that vector to estimate the missing token.

## Fine-tuning BERT for text classification

For a classification task, the input passes through BERT. The final hidden state of `[CLS]` is fed into a small **classification head**—usually a linear layer, followed by softmax for single-label multi-class classification. The BERT parameters and classification head are then fine-tuned using labelled task data.

```text
Input text → BERT encoder → final [CLS] hidden state → classification head → label probabilities
```

For binary sentiment analysis, the output labels might be `positive` and `negative`.

In BERT's masked language modelling task, the final hidden state at a selected token position is passed to a prediction head. This head includes feed-forward neural network and produces scores called logits for vocabulary tokens; softmax converts those scores into probabilities. Cross-entropy compares those probabilities with the original token.

## Feed-forward neural networks at a high level

A **feed-forward neural network (FNN)** moves information in one direction during its forward pass: from input to output. It has no recurrent loops or feedback connections, unlike recurrent neural networks (RNNs).

At a high level, an FNN contains:

- an **input layer**, which receives numerical input vectors;
- one or more **hidden layers**, which transform (Matrices) those vectors. This is where weights and biases are updated / adjusted; and
- an **output layer**, which produces predictions.

Training follows this cycle:

```text
input → forward pass → prediction → compare with target → loss → backpropagation → update weights and biases
```

### Logits and softmax

The scores produced before softmax are called **logits**. The prediction head produces one logit for every token in the vocabulary. A logit can be any real number, including a negative number; it is not yet a probability.

```text
Vocabulary token:   fish    meat     rice     vegetables
Logit:                5        4       -1         2
                         │
                         ▼
                      Softmax
                         │
                         ▼
Probability:         0.70     0.26    0.002      0.035
```

Softmax converts all logits into probabilities between 0 and 1 that sum to 1. A higher logit receives a higher probability, relative to the other logits. For `Cats are cute and they like to eat [MASK]`, `fish` has the highest probability, so it would be the model's most likely prediction. These numbers are illustrative.

**Note**: softmax is always used for multi-class classification (where an input belongs to exactly one category) but **not** multi-label classification where an input can be both politics and sports. For this sigmoid is used.


## References

- https://huggingface.co/learn/llm-course/chapter1/5
- https://mbrenndoerfer.com/writing/masked-language-modeling-bidirectional-understanding-bert
- https://medium.com/@sue_nlp/what-is-the-softmax-function-used-in-deep-learning-illustrated-in-an-easy-to-understand-way-8b937fe13d49
- https://www.geeksforgeeks.org/deep-learning/feedforward-neural-network/


