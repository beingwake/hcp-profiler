import torch
import pandas as pd
from torch.utils.data import DataLoader, Dataset, Subset
from sklearn.model_selection import train_test_split


class ServerLogDataset(Dataset):
    def __init__(self, file_path):
        self.raw_dataset = pd.read_csv(file_path)
        self.labels = self.raw_dataset["USERZIPCODE"]



    def __len__(self):
        return len(self.raw_dataset)
    
    def __getitem__(self, index):
        label = self.labels.loc[index]
        input = self.raw_dataset.loc[index, self.raw_dataset.columns != 'USERZIPCODE']
        return torch.tensor(input.to_numpy(), dtype=torch.float32), torch.tensor([label], dtype=torch.float32)
    

def train_val_dataset(dataset, val_split=0.20):
    train_idx, val_idx = train_test_split(list(range(len(dataset))), test_size=val_split)

    datasets = {}

    datasets["train"] = Subset(dataset, train_idx)
    datasets["val"] = Subset(dataset, val_idx)
    return datasets
