import torch
import torch.nn as nn
import tqdm

from torchvision.models.vgg import vgg16
from torchvision.datasets.cifar import CIFAR10
from torchvision.transforms import Compose, ToTensor, Resize
from torchvision.transforms import RandomHorizontalFlip, RandomCrop, Normalize
from torch.utils.data.dataloader import DataLoader
from torch.optim.adam import Adam

device = "cuda" if torch.cuda.is_available() else "cpu"
model = vgg16(pretrained=True)

fc = nn.Sequential(
    nn.Linear(25088, 4096),
    nn.ReLU(),
    nn.Dropout(0.5),
    nn.Linear(4096, 4096),
    nn.ReLU(),
    nn.Dropout(0.5),
    nn.Linear(4096, 10),
)

model.classifier = fc
model.to(device)

test_data = CIFAR10(root="./", train=True, download=True, transform=ToTensor())
test_data

test_data[0]

imgs = [item[0] for item in test_data]
imgs = torch.stack(imgs, dim=0).numpy()

mean_r = imgs[:, 0, :, :].mean()
mean_g = imgs[:, 1, :, :].mean()
mean_b = imgs[:, 2, :, :].mean()

std_r = imgs[:, 0, :, :].std()
std_g = imgs[:, 1, :, :].std()
std_b = imgs[:, 2, :, :].std()

transforms = Compose([
    Resize(224),
    RandomCrop((224, 224), padding=4),
    RandomHorizontalFlip(p=0.5),
    ToTensor(),
    Normalize(mean=(0.4914, 0.4822, 0.4465), std=(0.247, 0.243, 0.261))
])

train_data = CIFAR10(
    root='./',
    train=True,
    download=True,
    transform=transforms
)

test_data = CIFAR10(
    root='./',
    train=False,
    download=True,
    transform=transforms
)

train_loader = DataLoader(train_data, batch_size=32, shuffle=True)
test_loader = DataLoader(test_data, batch_size=32, shuffle=True)

lr = 0.004
optim = Adam(model.parameters(), lr=lr)

for epoch in range(30):
    iterator = tqdm.tqdm(train_loader)
    for data, label in iterator:
        optim.zero_grad()
        
        predicts = model(data.to(device))
        loss = nn.CrossEntropyLoss()(predicts, label.to(device))
        loss.backward()
        optim.step()

        iterator.set_description(f'epoch: {epoch + 1} loss: {loss.item()}')

torch.save(model.state_dict(), 'cifar10_pre.pth')

dict_model = torch.load('cifar10_pre.pth', map_location=device)
model.load_state_dict(dict_model)
num_corr = 0

with torch.no_grad():
    for data, label in test_data:
        output = model(data.to(device))
        predicts = output.data.max(1)[1]
        corr = predicts.eq(label.to(device)).sum().item()
        num_corr += corr

    print(num_corr / len(test_data))