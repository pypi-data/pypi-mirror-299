import os
import cv2
import numpy as np

import torch.utils.data
from torchvision import transforms
from torchvision.datasets import MNIST, FashionMNIST

from . import custom_dset


class BaseLoader(torch.utils.data.Dataset):
    def __init__(self, triplets, yaml_cfg ,transform=None):
        self.triplets = triplets
        self.transform = transform
        self.yaml_cfg = yaml_cfg

    def __getitem__(self, index):
        img1_pth, img2_pth, img3_pth = self.triplets[index]
        img1 = cv2.imread(img1_pth)
        img2 = cv2.imread(img2_pth)
        img3 = cv2.imread(img3_pth)

        try:
            img1 = cv2.resize(img1, (228, 228))
        except Exception as e:
            img1 = np.zeros((228, 228, 3), dtype=np.uint8)

        try:
            img2 = cv2.resize(img2, (228, 228))
        except Exception as e:
            img2 = np.zeros((228, 228, 3), dtype=np.uint8)

        try:
            img3 = cv2.resize(img3, (228, 228))
        except Exception as e:
            img3 = np.zeros((228, 228, 3), dtype=np.uint8)

        if self.transform is not None:
            img1 = self.transform(img1)
            img2 = self.transform(img2)
            img3 = self.transform(img3)

        return img1, img2, img3

    def __len__(self):
        return len(self.triplets)


class TripletMNISTLoader(BaseLoader):
    def __init__(self, triplets, yaml_cfg, transform=None):
        super(TripletMNISTLoader, self).__init__(triplets, yaml_cfg ,transform=transform)

    def __getitem__(self, index):
        img1, img2, img3 = self.triplets[index]
        img1 = np.expand_dims(img1, axis=2)
        img2 = np.expand_dims(img2, axis=2)
        img3 = np.expand_dims(img3, axis=2)

        if self.transform is not None:
            img1 = self.transform(img1)
            img2 = self.transform(img2)
            img3 = self.transform(img3)

        return img1, img2, img3


def get_loader(args, yaml_cfg):
    train_data_loader = None
    test_data_loader = None

    kwargs = {'num_workers': 1, 'pin_memory': True} if args["cuda"] else {}

    train_triplets = []
    test_triplets = []

    dset_obj = None
    loader = BaseLoader
    means = (0.485, 0.456, 0.406)
    stds = (0.229, 0.224, 0.225)

    if args["dataset"] == 'custom':
        dset_obj = custom_dset.Custom(yaml_cfg)


    dset_obj.load()
    for i in range(args["num_train_samples"]):
        pos_anchor_img, pos_img, neg_img = dset_obj.getTriplet()
        train_triplets.append([pos_anchor_img, pos_img, neg_img])
    for i in range(args["num_test_samples"]):
        pos_anchor_img, pos_img, neg_img = dset_obj.getTriplet(split='test')
        test_triplets.append([pos_anchor_img, pos_img, neg_img])

    train_data_loader = torch.utils.data.DataLoader(
        loader(train_triplets,
               yaml_cfg,
               transform=transforms.Compose([
                   transforms.ToTensor(),
                   transforms.Normalize(means, stds)
               ])),
        batch_size=args["batch_size"], shuffle=True, **kwargs)
    test_data_loader = torch.utils.data.DataLoader(
        loader(test_triplets,
                yaml_cfg,
               transform=transforms.Compose([
                   transforms.ToTensor(),
                   transforms.Normalize(means, stds)
               ])),
        batch_size=args["batch_size"], shuffle=True, **kwargs)

    return train_data_loader, test_data_loader
