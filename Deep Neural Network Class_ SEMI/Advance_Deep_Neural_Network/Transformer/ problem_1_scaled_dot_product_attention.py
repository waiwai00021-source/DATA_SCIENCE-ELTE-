"""
ADND Practice Module 1B - Transformers
Problem 1: Scaled Dot-Product Attention
========================================

Implement the attention mechanism used in Transformers:

    Attention(Q, K, V) = softmax(Q K^T / sqrt(d_k)) V

Your function should:
  - Accept Q, K, V tensors of shape (batch, heads, seq_len, d_k)
  - Accept an optional boolean mask where True means "this position should be MASKED (ignored)"
  - Return a tuple: (output, attention_weights)
    - output: shape (batch, heads, seq_len, d_k)
    - attention_weights: shape (batch, heads, seq_len, seq_len)

"""
import torch
import torch.nn.functional as F
import math


def scaled_dot_product_attention(Q, K, V, mask):
    """
    Compute scaled dot-product attention.

    Args:
        Q: Query tensor, shape (batch, heads, seq_len, d_k)
        K: Key tensor, shape (batch, heads, seq_len, d_k)
        V: Value tensor, shape (batch, heads, seq_len, d_k)
        mask: Optional boolean mask, shape broadcastable to
              (batch, heads, seq_len, seq_len). True indicates
              positions that should be masked.

    Returns:
        output: Attention output, shape (batch, heads, seq_len, d_k)
        weights: Attention weights after softmax, shape (batch, heads, seq_len, seq_len)
    """
    # TODO: Get d_k from Query tensor
    # d_k = ...

    # TODO: Compute attention scores
    # scores shape: (batch, heads, seq_len, seq_len)
    # scores = ...

    # TODO: If mask is provided, fill masked positions with -inf
    # if mask is not None:
    #     scores = ...

    # TODO: Apply softmax
    # weights = ...

    # TODO: Compute the weighted sum: weights @ V
    # output = ...

    # TODO: Return (output, weights)
    raise NotImplementedError("Implement scaled_dot_product_attention")
