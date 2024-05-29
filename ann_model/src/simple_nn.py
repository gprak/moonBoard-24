from typing import List
from typing import Tuple

import numpy as np
import pandas as pd
import torch
import torch.nn as nn
import torch.nn.functional as f
from sklearn.model_selection import train_test_split


class Model(nn.Module):
    def __init__(
        self,
        h: tuple = (40, 20, 10),
        in_features: int = 198,
        out_features: int = 10,
    ) -> None:
        super().__init__()

        self.fc = []
        self.fc.append(nn.Linear(in_features, h[0]))  # input layer
        for i in range(1, len(h)):
            self.fc.append(nn.Linear(h[i - 1], h[i]))  # hidden layer

        self.out = nn.Linear(h[-1], out_features)  # output layer

    def forward(self, x: torch.tensor) -> torch.tensor:
        for i in range(len(self.fc)):
            cf = self.fc[i]
            x = f.tanh(cf(x))

        x = self.out(x)
        return x


class SimpleNN:
    def __init__(self, df: pd.DataFrame) -> None:
        super().__init__()

        self.df = df
        self.x_train, self.x_test, self.y_train, self.y_test = (
            SimpleNN.split_dataset(self.df, 0.2)
        )

    @staticmethod
    def split_dataset(
        df: pd.DataFrame, fraction: float
    ) -> Tuple[
        torch.FloatTensor,
        torch.FloatTensor,
        torch.LongTensor,
        torch.LongTensor,
    ]:
        x = df.drop(["grade"], axis=1).values
        y = df["grade"].values

        xtrain, xtest, ytrain, ytest = train_test_split(
            x, y, test_size=fraction, random_state=33
        )

        x_train = torch.FloatTensor(np.array(xtrain.tolist()))
        x_test = torch.FloatTensor(np.array(xtest.tolist()))

        y_train = torch.LongTensor(np.array(ytrain.tolist()))
        y_test = torch.LongTensor(np.array(ytest.tolist()))

        return x_train, x_test, y_train, y_test

    def train_model(
        self, model: Model, lr: float, epochs: int
    ) -> Tuple[List[float], float, int]:
        torch.manual_seed(32)
        optimizer = torch.optim.Adam(model.parameters(), lr=lr)
        criterion = nn.CrossEntropyLoss()

        epochs = epochs
        losses_train = []

        for i in range(epochs):
            i += 1
            y_pred = model.forward(self.x_train)
            loss_train = criterion(y_pred, self.y_train)
            losses_train.append(loss_train.detach().numpy())

            optimizer.zero_grad()
            loss_train.backward()
            optimizer.step()

        # TO EVALUATE THE ENTIRE TEST SET
        with torch.no_grad():
            y_val = model.forward(self.x_test)
            loss_test = criterion(y_val, self.y_test)

        correct = 0
        with torch.no_grad():
            for i, data in enumerate(self.x_test):
                y_val = model.forward(data)
                # print(f'{i+1:2}. {str(y_val):38}  {y_test[i]}')
                # print(y_val.argmax().item(), y_test[i],y_val.argmax().item()
                # == y_test[i])
                if y_val.argmax().item() == self.y_test[i]:
                    correct += 1

        return losses_train, loss_test, correct

    def run_model(
        self, h: tuple, lr: float, epochs: int
    ) -> Tuple[List[float], float, int]:
        return self.train_model(Model(h), lr=lr, epochs=epochs)
