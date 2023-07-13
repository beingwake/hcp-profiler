import os
import torch
from torch import nn
from torch.utils.data import DataLoader

class NeuralNetwork(nn.Module):
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        
        self.linear1 = nn.Linear(45,45)
        self.activation = nn.ReLU()
        self.linear2 = nn.Linear(45,45)
        self.linear3 = nn.Linear(45, 1)

    def forward(self, x):
        x = self.linear1(x)
        x = self.activation(x)
        x = self.linear2(x)
        x = self.activation(x)
        x = self.linear3(x)

        return x