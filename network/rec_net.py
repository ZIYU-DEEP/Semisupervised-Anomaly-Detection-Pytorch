"""
Title: LSTM_net.py
Description: The LSTM network.
Author: Lek'Sai Ye, University of Chicago
"""

import torch
import torch.nn as nn
import torch.nn.functional as F
from base_net import BaseNet


class RecEncoder(BaseNet):
    def __init__(self, rep_dim=32):
        super().__init__()

        self.rep_dim = rep_dim
        self.lstm1 = nn.LSTM(128, 64, num_layers=3, batch_first=True)
        self.fc1 = nn.Linear(64 * 100, self.rep_dim, bias=False)

    def forward(self, x):
        x, _ = self.lstm1(x)
        x = x.reshape(x.size(0), 64 * 100).contiguous()
        x = self.fc1(x)
        return x


class RecDecoder(BaseNet):

    def __init__(self, rep_dim=32):
        super().__init__()

        self.rep_dim = rep_dim

        # Decoder network
        self.lstm1 = nn.LSTM(64, 128, num_layers=3, batch_first=True)
        self.fc1 = nn.Linear(self.rep_dim, 64 * 100)

    def forward(self, x):
        x = self.fc1(x)
        x = x.view(x.size(0), 100, 64).contiguous()
        x, _ = self.lstm1(x)
        x = torch.sigmoid(x)
        return x


class RecAutoencoder(BaseNet):
    def __init__(self, rep_dim=32):
        super().__init__()

        self.rep_dim = rep_dim
        self.encoder = RecEncoder(rep_dim=rep_dim)
        self.decoder = RecDecoder(rep_dim=rep_dim)

    def forward(self, x):
        x = self.encoder(x)
        x = self.decoder(x)
        return x
