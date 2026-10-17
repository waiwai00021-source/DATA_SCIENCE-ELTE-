"""
ADND Practice Module 1A - Transformers
Problem 2: Multi-Head Attention Module
=======================================

Implement multi-head attention as an nn.Module:

  1.  Project Q, K, V through separate linear layers (W_Q, W_K, W_V)
  2.  Split the projected tensors into `num_heads` heads
  3.  Apply scaled_dot_product_attention (from problem 1) to each head in parallel
  4.  Concatenate the head outputs
  5.  Project through a final linear layer (W_O)

Your class must:
Accept inputs of shape (batch, seq_len, d_model) and return the same shape

You may use your solution from problem 1.
"""

import math
import torch
import torch.nn as nn

# Import your scaled dot product attention implementation here

from problem_1 import scaled_dot_product_attention

class MultiHeadAttention(nn.Module):
    """
    Multi-Head Attention mechanism.

    Args:
        d_model: Total model dimension
        num_heads: Number of parallel attention heads
    """

    def __init__(self, d_model, num_heads):
        super().__init__()

        if d_model % num_heads != 0:
            raise ValueError("d_model must be divisible by num_heads")

        self.d_model = d_model
        self.num_heads = num_heads
        self.d_k = d_model // num_heads

        # TODO: Create four linear layers
        # self.W_Q = nn.Linear(...)
        # self.W_K = nn.Linear(...)
        # self.W_V = nn.Linear(...)
        # self.W_O = nn.Linear(...)

        self.W_Q = nn.Linear(d_model, d_model)
        self.W_K = nn.Linear(d_model, d_model)
        self.W_V = nn.Linear(d_model, d_model)
        self.W_O = nn.Linear(d_model, d_model)

    def forward(self, query, key, value, mask=None):
        """
        Args:
            query: (batch, seq_len, d_model)
            key:   (batch, seq_len, d_model)
            value: (batch, seq_len, d_model)
            mask:  Optional boolean mask

        Returns:
            output: (batch, seq_len, d_model)
        """
        # TODO: Get the batch size
        # batch_size = ...
        batch_size = query.size(0)
        # TODO: Project inputs through W_Q, W_K, W_V
        # Q = self.W_Q(query)   # (batch, seq, d_model)
        # K = ...
        # V = ...

        Q = self.W_Q(query)   # (batch, seq, d_model)
        K = self.W_K(key)     # (batch, seq, d_model)
        V = self.W_V(value)   # (batch, seq, d_model)

        # TODO: Reshape from (batch, seq, d_model) to (batch, num_heads, seq, d_k)
        # Q = ...
        # K = ...
        # V = ...

        Q = Q.view(batch_size, -1, self.num_heads, self.d_k).transpose(1, 2)  # (batch, num_heads, seq, d_k)
        K = K.view(batch_size, -1, self.num_heads, self.d_k).transpose(1, 2)  # (batch, num_heads, seq, d_k)        
        V = V.view(batch_size, -1, self.num_heads, self.d_k).transpose(1, 2)  # (batch, num_heads, seq, d_k)    

        # TODO: Apply scaled dot-product attention (from problem 1)
        # attn_output, _ = scaled_dot_product_attention(Q, K, V, mask)

        attn_output, _ = scaled_dot_product_attention(Q, K, V, mask)  # (batch, num_heads, seq, d_k)    

        # TODO: Reshape back: (batch, num_heads, seq, d_k) -> (batch, seq, d_model)
        # attn_output = ...

        attn_output = attn_output.transpose(1, 2).contiguous().view(batch_size, -1, self.d_model)  # (batch, seq, d_model)      

        # TODO: Final projection through W_O
        # output = self.W_O(attn_output)

        output = self.W_O(attn_output)  # (batch, seq, d_model)

        # TODO: return output
        return output


# Testing part 

batch_size = 2
seq_len = 10
d_model = 64
num_heads = 8

mha = MultiHeadAttention(d_model, num_heads)

x = torch.randn(batch_size, seq_len, d_model)

output = mha(x, x, x)

print("Input shape: ", x.shape)
print("Output shape:", output.shape)