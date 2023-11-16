from torch.utils.data import DataLoader
from tqdm import tqdm
from model.MEFL import MEFARG
from dataset import *
from utils import *
import glob
from PIL import Image
from torch.utils.data import Dataset
import os

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

def get_dataloader(batch_size, crop_size):
    print('==> Preparing data...')
    base_data = glob.glob('./data/*/*/*png')
    dataset = BaseDataset(base_data, transform=image_test(crop_size=crop_size))
    testloader = DataLoader(dataset, batch_size=batch_size, shuffle=False, num_workers=8)

    return testloader

# BP4D AU1 AU2 AU4 AU6 AU7 AU10 AU12 AU14 AU15 AU17 AU23 AU24
# DISFA AU9 AU25 AU26
def save_au(pathes, aues, pretrained_type='BP4D'):
    for i in range(len(pathes)):
        path = pathes[i]
        au = aues[i].squeeze(-1)

        s = path.split('/')
        data_type, group, pid, img_id = s[-4], s[-3], s[-2], s[-1]
        img_id = img_id.split('.')[0]
        save_path = os.path.join('./data/extracted_au', data_type, group, pid, img_id + '.pth')
        if pretrained_type == 'DISFA':
            au = au[:, [0, 6, 7]]
        torch.save(au, save_path)

    return


def extract(batch_size, crop_size, checkpoint_pth, pretrained_type):
    testloader = get_dataloader(batch_size, crop_size)
    num_classes = 12 if pretrained_type == 'BP4D' else 8
    model = MEFARG(num_classes=num_classes, backbone='swin_transformer_base')
    model = load_state_dict(model, checkpoint_pth)

    if torch.cuda.is_available():
        model = nn.DataParallel(model).cuda()

    with torch.no_grad():
        for i, data in enumerate(tqdm(testloader)):
            inputs, pathes = data
            inputs = inputs.cuda()

            outputs, _ = model(inputs)

            save_au(outputs, pathes)

# ---------------------------------------------------------------------------------


if __name__=="__main__":
    extract(128, 224, '/home/extract/ME-GraphAU/checkpoints/MEFARG_swin_base_BP4D_fold1.pth', 'BP4D')

