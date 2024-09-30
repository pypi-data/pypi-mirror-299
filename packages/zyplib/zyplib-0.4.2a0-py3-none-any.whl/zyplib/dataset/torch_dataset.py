from typing import Union

import numpy as np
import torch
from torch.utils.data import Dataset


class BasicXyDataset(Dataset):
    def __init__(
        self,
        data: Union[np.ndarray, torch.Tensor],
        labels: Union[np.ndarray, torch.Tensor],
    ):
        if isinstance(data, np.ndarray):
            data = torch.from_numpy(data)
        if isinstance(labels, np.ndarray):
            labels = torch.from_numpy(labels)
        self.data = data
        self.labels = labels

    def __len__(self):
        return len(self.data)

    def __getitem__(self, idx):
        return self.data[idx], self.labels[idx]
