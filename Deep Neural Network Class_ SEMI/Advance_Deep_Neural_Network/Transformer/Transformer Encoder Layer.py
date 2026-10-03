"""
ADND Practice Module 1B: Transformers
Problem 4: Transformer Encoder Layer
======================================

Implement a single Transformer encoder layer containing:

  1.  Multi-head self-attention (from T2) + residual connection + LayerNorm
  2.  Position-wise feed-forward network + residual connection + LayerNorm

The feed-forward network consists of two linear layers with a ReLU activation:
    FFN(x) = Linear_2(ReLU(Linear_1(x)))
    where Linear_1: d_model -> d_ff  and  Linear_2: d_ff -> d_model

You must choose either Post-LN or Pre-LN (state which in a comment):
  - Post-LN:  output = LayerNorm(x + sublayer(x))
  - Pre-LN:   output = x + sublayer(LayerNorm(x))

You may import MultiHeadAttention from your previous solution.
"""

import torch
import torch.nn as nn

# Import your MultiHeadAttention implementation here

from problem_2 import MultiHeadAttention

class TransformerEncoderLayer(nn.Module):
    """
    A single Transformer encoder layer.

    Args:
        d_model:   Model dimension
        num_heads: Number of attention heads
        d_ff:      Hidden dimension of the feed-forward network
        dropout:   Dropout probability
    """

    # TODO: Specify which normalisation order you are using
    # NORMALISATION_ORDER = "post-ln"  # or "pre-ln"

    NORMALISATION_ORDER = "post-ln"  # or "pre-ln"

    def __init__(self, d_model, num_heads, d_ff, dropout):
        super().__init__()

        # TODO: Multi-head self-attention
        self.attention = MultiHeadAttention(d_model, num_heads)

        # TODO: Feed-forward network
        self.feed_forward = nn.Sequential(
            nn.Linear(d_model, d_ff),
            nn.ReLU(),
            nn.Linear(d_ff, d_model)
        )

        # TODO: Layer norms (you need exactly 2)
        self.norm1 = nn.LayerNorm(d_model)
        self.norm2 = nn.LayerNorm(d_model)

        # TODO: Dropout layers
        self.dropout1 = nn.Dropout(dropout)
        self.dropout2 = nn.Dropout(dropout)

    def forward(self, src, mask = None):
        """
        Args:
            src:  Input tensor of shape (batch, seq_len, d_model)
            mask: Optional attention mask

        Returns:
            Output tensor of shape (batch, seq_len, d_model)
        """
        # Sub-layer 1: Multi-head self-attention + residual + norm
        if self.NORMALISATION_ORDER == "post-ln":
            src = self.norm1(src + self.dropout1(self.attention(src, src, src, mask)))
        else:
            src = src + self.dropout1(self.attention(self.norm1(src), self.norm1(src), self.norm1(src), mask))

        # Sub-layer 2: Feed-forward + residual + norm
        if self.NORMALISATION_ORDER == "post-ln":
            src = self.norm2(src + self.dropout2(self.feed_forward(src)))
        else:
            src = src + self.dropout2(self.feed_forward(self.norm2(src)))

        # TODO: return src
        return src
