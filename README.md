# Engineering Journal

## HuggingFace NLP Course

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
