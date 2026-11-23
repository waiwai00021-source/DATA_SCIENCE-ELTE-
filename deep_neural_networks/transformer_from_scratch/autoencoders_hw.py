"""
  Problem 1: Small Auto-Encoder on Synthetic Data
  Problem 2: Basic Auto-Encoder on MNIST
  Problem 3: Denoising Auto-Encoder

  Your task is to fill in each function or code segment makers with #TODO.

  To test your implementation you can run
  >>> python autoencoders.py

  All tasks are small enough to run quickly on your local CPU. 
"""

import math, sys
import torch
import torch.nn as nn
import torch.nn.functional as F
from torch.utils.data import DataLoader, TensorDataset

import torchvision
import torchvision.transforms as transforms

torch.manual_seed(11)
DEVICE = torch.device("cpu")

_mnist_cache = {}

def get_mnist_subset(n_train=1000, n_test=200):
    if "train" not in _mnist_cache:
        tf = transforms.ToTensor()  
        full_train = torchvision.datasets.MNIST(
            root="./data", train=True, download=True, transform=tf
        )
        full_test = torchvision.datasets.MNIST(
            root="./data", train=False, download=True, transform=tf
        )
        _mnist_cache["train"] = full_train
        _mnist_cache["test"] = full_test

    train_ds = torch.utils.data.Subset(_mnist_cache["train"], range(n_train))
    test_ds = torch.utils.data.Subset(_mnist_cache["test"], range(n_test))
    train_loader = DataLoader(train_ds, batch_size=64, shuffle=True)
    test_loader = DataLoader(test_ds, batch_size=200, shuffle=False)
    return train_loader, test_loader

#------------------------------------------------------------                                                            
# Problem 1: Small Auto-Encoder on Synthetic Data
#------------------------------------------------------------
"""
TASK:
Complete the SimpleAE class:
  1. Encoder: Linear(input_dim, 32) -> ReLU -> Linear(32, latent_dim)
  2. Decoder: Linear(latent_dim, 32) -> ReLU -> Linear(32, input_dim)
  3. Implement encode, decode, and forward functions
"""

def make_data(n=600):
    t = 1.5 * math.pi * (1 + 2 * torch.rand(n))
    x = t * torch.cos(t)
    y = 30 * torch.rand(n)
    z = t * torch.sin(t)
    data = torch.stack([x, y, z], dim=1)
    data = (data - data.mean(0)) / data.std(0)
    return data


class SimpleAE(nn.Module):
    """auto-encoder with one hidden layer"""

    def __init__(self, input_dim=3, latent_dim=2, hidden=32):
        super().__init__()
        self.encoder = nn.Sequential(
            nn.Linear(input_dim, hidden),
            nn.ReLU(),
            nn.Linear(hidden, latent_dim)
        )
        self.decoder = nn.Sequential(
            nn.Linear(latent_dim, hidden),
            nn.ReLU(),
            nn.Linear(hidden, input_dim)
        )

    def encode(self, x):
        return self.encoder(x)

    def decode(self, z):
        return self.decoder(z)

    def forward(self, x):
        return self.decode(self.encode(x))


def validate_p1():
    print("Problem 1: Simple Auto-Encoder on Synth Data")
    torch.manual_seed(11)
    data = make_data(600)
    dataset = TensorDataset(data)
    loader = DataLoader(dataset, batch_size=64, shuffle=True)

    model = SimpleAE(input_dim=3, latent_dim=2)
    opt = torch.optim.Adam(model.parameters(), lr=1e-3)

    for epoch in range(80):
        for (batch,) in loader:
            x_hat = model(batch)
            loss = F.mse_loss(x_hat, batch)
            opt.zero_grad()
            loss.backward()
            opt.step()

    model.eval()
    with torch.no_grad():
        x_hat = model(data)
        mse = F.mse_loss(x_hat, data).item()

    print(f"Final reconstruction MSE: {mse:.4f}")

#------------------------------------------------------------
# Problem 2: Auto-Encoder on MNIST with Bottleneck
#------------------------------------------------------------
"""
Architecture:
  Encoder: [784, 256, 64, 2]
  Decoder: [2, 64, 256, 784]

All hidden layers use ReLU.  The final decoder layer uses Sigmoid.

TASK
1. Complete MnistAE (encoder + decoder).
2. Complete train_one_epoch function to complete one epoch of training with BCE loss.

"""

class MnistAE(nn.Module):
    def __init__(self, latent_dim=2):
        super().__init__()
        self.encoder = nn.Sequential(
            nn.Linear(784, 256),
            nn.ReLU(),
            nn.Linear(256, 64),
            nn.ReLU(),
            nn.Linear(64, latent_dim)
        )
        self.decoder = nn.Sequential(
            nn.Linear(latent_dim, 64),
            nn.ReLU(),
            nn.Linear(64, 256),
            nn.ReLU(),
            nn.Linear(256, 784),
            nn.Sigmoid()
        )

    def encode(self, x):
        return self.encoder(x)

    def decode(self, z):
        return self.decoder(z)

    def forward(self, x):
        return self.decode(self.encode(x))


def train_one_epoch(model, loader, optimiser):
    """Train for one epoch. Return average loss."""
    model.train()
    total_loss = 0.0
    n = 0
    for imgs, _ in loader:
        x = imgs.view(-1, 784)
        x_hat = model(x)
        loss = F.binary_cross_entropy(x_hat, x)
        optimiser.zero_grad()
        loss.backward()
        optimiser.step()
        total_loss += loss.item() * x.size(0)
        n += x.size(0)

    return total_loss / n


def validate_p2():
    print("Problem 2: MNIST Auto-Encoder")
    torch.manual_seed(42)
    train_loader, test_loader = get_mnist_subset()
    model = MnistAE(latent_dim=2)
    opt = torch.optim.Adam(model.parameters(), lr=1e-3)

    for epoch in range(20):
        avg_loss = train_one_epoch(model, train_loader, opt)
    print(f"Train loss after 20 epochs: {avg_loss:.4f}")

    model.eval()
    with torch.no_grad():
        for imgs, labels in test_loader:
            x = imgs.view(-1, 784)
            x_hat = model(x)
            test_loss = F.binary_cross_entropy(x_hat, x).item()
            break
    print(f"Test reconstruction BCE: {test_loss:.4f}")

    return model

# Problem 3: Denoising Auto-Encoder

"""
A denoising AE (DAE) receives corrupted input \tilde{x} but is trained to
reconstruct the clean input x. This forces the model to learn robust
features rather than memorising identity.

TASK:
1. Implement add_gaussian_noise(x, std) add noise, ensure the result is in the range [0, 1].
2. Complete train_one_epoch_denoising function
"""

def add_gaussian_noise(x, std):
    """Add Gaussian noise to x, clip to [0, 1]"""
    noise = torch.randn_like(x) * std
    noisy_x = x + noise
    return torch.clamp(noisy_x, 0.0, 1.0)


def train_one_epoch_denoising(model, loader, optimiser, noise_fn):
    model.train()
    total_loss = 0.0
    n = 0
    for imgs, _ in loader:
        x_clean = imgs.view(-1, 784)
        x_noisy = noise_fn(x_clean)
        x_hat = model(x_noisy)
        loss = F.binary_cross_entropy(x_hat, x_clean)
        optimiser.zero_grad()
        loss.backward()
        optimiser.step()
        total_loss += loss.item() * x_clean.size(0)
        n += x_clean.size(0)    
    return total_loss / n


def validate_p3():
    print("Problem 3: Denoising Auto-Encoder")
    torch.manual_seed(11)

    #  Train DAE 
    train_loader, test_loader = get_mnist_subset()
    model = MnistAE(latent_dim=16) 
    opt = torch.optim.Adam(model.parameters(), lr=1e-3)
    noise_fn = lambda x: add_gaussian_noise(x, std=0.4)

    for epoch in range(25):
        train_one_epoch_denoising(model, train_loader, opt, noise_fn)

    model.eval()
    with torch.no_grad():
        for imgs, _ in test_loader:
            x_clean = imgs.view(-1, 784)
            x_noisy = noise_fn(x_clean)
            x_hat = model(x_noisy)
            test_loss = F.binary_cross_entropy(x_hat, x_clean).item()
            break
        
    print(f"Denoising test: {test_loss:.4f}")

PROBLEMS = {
    1: ("Toy Data Auto-Encoder", validate_p1),
    2: ("MNIST Auto-Encoder", validate_p2),
    3: ("Denoising Auto-Encoder", validate_p3)
}

if __name__ == "__main__":
    for num, (name, fn) in PROBLEMS.items():
        fn()
