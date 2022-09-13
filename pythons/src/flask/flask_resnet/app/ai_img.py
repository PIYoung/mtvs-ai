import torch
import torch.nn as nn
from torchvision import models, transforms
from PIL import Image

class_names = ["마동석", "이국주", "카리나"]
device = torch.device("cuda" if torch.cuda.is_available else "cpu")
transforms_test = transforms.Compose(
    [
        transforms.Resize((224, 224)),
        transforms.ToTensor(),
        transforms.Normalize([0.485, 0.456, 0.406], [0.229, 0.224, 0.225]),
    ]
)

model = models.resnet34(pretrained=True)
model.fc = nn.Linear(512, 3)
model.load_state_dict(torch.load("app/model_dict.pth"))
model.eval()
model = model.to(device)


def ai_image(img):
    image = Image.open(img)
    image = transforms_test(image).unsqueeze(0).to(device)

    with torch.no_grad():
        outputs = model(image)
        _, preds = torch.max(outputs, 1)

        print(preds)
        print(class_names[preds[0]])

        return class_names[preds[0]]
