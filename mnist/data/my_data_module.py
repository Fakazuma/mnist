import os
from typing import Optional

import lightning.pytorch as pl
import torch
from torch.utils.data.dataset import random_split
from torchvision.datasets import MNIST
from torchvision.transforms import ToTensor


class MyDataModule(pl.LightningDataModule):
    def __init__(
        self,
        data_dir: str,
        val_part: float,
        batch_size: int,
        dataloader_num_workers: int,
    ):
        super().__init__()
        self.save_hyperparameters()
        self.data_dir = data_dir
        self.val_part = val_part
        self.dataloader_num_workers = dataloader_num_workers
        self.batch_size = batch_size

    def prepare_data(self):
        MNIST(root=self.data_dir, train=True, download=True)  # train + val
        MNIST(root=self.data_dir, train=False, download=True)  # test

    def setup(self, stage: Optional[str] = None):
        self.mnist_test = MNIST(self.data_dir, train=False, transform=ToTensor())
        mnist_full = MNIST(self.data_dir, train=True, transform=ToTensor())
        self.mnist_train, self.mnist_val = random_split(
            mnist_full,
            [1 - self.val_part, self.val_part],
            generator=torch.Generator().manual_seed(42),
        )

    def train_dataloader(self) -> torch.utils.data.DataLoader:
        return torch.utils.data.DataLoader(
            self.mnist_train,
            batch_size=self.batch_size,
            shuffle=True,
            num_workers=self.dataloader_num_workers,
        )

    def val_dataloader(self) -> torch.utils.data.DataLoader:
        return torch.utils.data.DataLoader(
            self.mnist_val,
            batch_size=self.batch_size,
            shuffle=False,
            num_workers=self.dataloader_num_workers,
        )

    def test_dataloader(self) -> torch.utils.data.DataLoader:
        return torch.utils.data.DataLoader(
            self.mnist_test,
            batch_size=self.batch_size,
            shuffle=False,
            num_workers=self.dataloader_num_workers,
        )
