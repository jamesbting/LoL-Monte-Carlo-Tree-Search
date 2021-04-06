import torch
import torch.nn as nn

class ChampionNet(nn.Module):
    #constructor
    def __init__(self, num_units=128, dropout_rate=0.5):
        super(ChampionNet, self).__init__() #superclass constructor
        self.fc1 = nn.Linear(154, num_units)
        self.fc2 = nn.Linear(num_units,num_units)
        self.fc3 = nn.Linear(num_units,2)
        self.nonlin = nn.ReLU()
        self.dropout = nn.Dropout(p=dropout_rate)

    def forward(self, x):
        x = self.nonlin(self.fc1(x))
        x = self.nonlin(self.fc2(x))
        x = self.dropout(x)
        x = self.fc3(x)
        return x
