import glob
import json
import random

import numpy as np
import torch
from PIL import Image

def norm(image):
    return (image / 127.5) - 1.0

def denorm(image):
    return (image + 1.0) * 127.5

def augment(dt_im, eh_im):
    # Random interpolation
    a = random.random()
    dt_im = dt_im * a + eh_im * (1 - a)

    # Random flip left right
    if random.random() < 0.25:
        dt_im = np.fliplr(dt_im)
        eh_im = np.fliplr(eh_im)

    # Random flip up down
    if random.random() < 0.25:
        dt_im = np.flipud(dt_im)
        eh_im = np.flipud(eh_im)

    return dt_im, eh_im

# CHANGES MADE FOR COMBINING DATASETS
class CombinedDataset(torch.utils.data.Dataset):
    def __init__(self, data_root, im_size, split, paired=True):
        super(CombinedDataset, self).__init__()

        self.data_root = data_root
        self.im_size = im_size
        self.split = split
        self.paired = paired

        # Load JSON of splits
        names = json.load(open(f"{self.data_root}/splits.json", "r"))[self.split]

        # Build image paths
        self.dt_ims = [f"{self.data_root}/{n.replace('trainB', 'trainA')}" for n in names]
        self.eh_ims = [f"{self.data_root}/{n}" for n in names]

        print(f"Total {len(self.dt_ims)} data")

    def __getitem__(self, index):
        # Read and resize image pair
        dt_im = Image.open(self.dt_ims[index]).convert("RGB")
        eh_im = Image.open(self.eh_ims[index]).convert("RGB")
        dt_im = dt_im.resize(self.im_size)
        eh_im = eh_im.resize(self.im_size)

        # Transfrom image pair to float32 np.ndarray
        dt_im = np.array(dt_im, dtype=np.float32)
        eh_im = np.array(eh_im, dtype=np.float32)

        # Augment image pair
        if self.split == "train":
            dt_im, eh_im = augment(dt_im, eh_im)

        # Transfrom image pair to (C, H, W) torch.Tensor
        dt_im = torch.Tensor(norm(dt_im)).permute(2, 0, 1)
        eh_im = torch.Tensor(norm(eh_im)).permute(2, 0, 1)
        return dt_im, eh_im

    def __len__(self):
        return len(self.dt_ims)

class TestDataset(torch.utils.data.Dataset):
    def __init__(self, data_root, im_size):
        super(TestDataset, self).__init__()

        self.data_root = data_root
        self.im_size = im_size
        self.ims = glob.glob(f"{self.data_root}/*")

    def __getitem__(self, index):
        # Read and resize image
        path = self.ims[index]
        im = Image.open(path).convert("RGB")
        im = im.resize(self.im_size)

        # Transfrom image to float32 np.ndarray
        im = np.array(im, dtype=np.float32)

        # Transfrom image to (C, H, W) torch.Tensor
        im = torch.Tensor(norm(im)).permute(2, 0, 1)
        return path, im

    def __len__(self):
        return len(self.ims)

if __name__ == "__main__":
    # Example usage for the combined dataset
    dataset = CombinedDataset(
        data_root="../data/EUVP Dataset/Paired", im_size=(256, 256), split="train", paired=True)
    image, target = dataset[0]
