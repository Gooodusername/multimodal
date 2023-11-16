from PIL import Image
from torch.utils.data import Dataset

class BaseDataset(Dataset):
    def __init__(self, image_list, transform=None):

        self.imgs = image_list
        self.transform = transform

    def __getitem__(self, index):
        path, target = self.imgs[index]
        img = Image.open(path)
        if self.transform is not None:
            img = self.transform(img)

        return img, path

    def __len__(self):
        return len(self.imgs)