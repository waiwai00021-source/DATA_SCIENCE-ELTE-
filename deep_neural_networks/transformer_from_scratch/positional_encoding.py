"""
ADND Practice Module 1B: Transformers
Problem 3: Positional Encoding
================================

Implement sinusoidal positional encoding

    PE(pos, 2i)   = sin(pos / 10000^(2i / d_model))
    PE(pos, 2i+1) = cos(pos / 10000^(2i / d_model))

Your class must:
  - Pre-compute the full encoding matrix in __init__ (up to max_len positions)
  - Store it as a buffer (not a parameter) using self.register_buffer
  - In forward(), add the encoding to the input embedding 
  - Support sequences up to max_len=5000

"""

import math
from sympy import python
import torch
import torch.nn as nn


class PositionalEncoding(nn.Module):
    """
    Sinusoidal positional encoding.

    Args:
        d_model:  Embedding dimension
        max_len:  Maximum sequence length to pre-compute
    """

    def __init__(self, d_model, max_len = 5000):
        super().__init__()

        # TODO: Create a (max_len, d_model) tensor of positional encodings
        # Step 1: Create a positions vector: [0, 1, 2, ..., max_len - 1]
        #         shape: (max_len, 1)
        # position = ...

        position = torch.arange(max_len).unsqueeze(1).float()  # shape: (max_len, 1)    

        # Step 2: Create the dimension index: [0, 2, 4, ..., d_model - 2]
        #         and compute the denominator
        #         shape: (d_model // 2,)
        # div_term = ...

        div_term = torch.exp(torch.arange(0, d_model, 2).float() * (-math.log(10000.0) / d_model))  # shape: (d_model // 2,)

        # Step 3: Create the PE matrix (max_len, d_model) filled with zeros

        pe = torch.zeros(max_len, d_model)  # shape: (max_len, d_model)

        # Step 4: Fill even indices with sin, odd indices with cos
        
        pe[:, 0::2] = torch.sin(position * div_term)  # even indices
        pe[:, 1::2] = torch.cos(position * div_term)  # odd

        # Step 5: Register as a buffer (NOT a parameter)
        #         This ensures it moves to the correct device with the model
        #         but is not updated by the optimiser
        # self.register_buffer('pe', pe)

        self.register_buffer('pe', pe)

    def forward(self, x):
        """
        Add positional encoding to input embeddings.

        Args:
            x: Input tensor of shape (batch, seq_len, d_model)

        Returns:
            Tensor of shape (batch, seq_len, d_model) with PE added
        """
        # TODO: Add the positional encoding for the first seq_len positions
        x = x + self.pe[:x.size(1), :].unsqueeze(0)
        return x


      # Testing the implementation

if __name__ == "__main__":
    d_model = 512
    max_len = 5000
    pe = PositionalEncoding(d_model, max_len)

    # Test with a batch of embeddings
    batch_size = 2
    seq_len = 10
    x = torch.zeros(batch_size, seq_len, d_model)
    x_pe = pe(x)

    print("Input shape:", x.shape)
    print("Output shape:", x_pe.shape)
