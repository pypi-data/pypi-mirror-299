from typing import List, Callable

from PIL import Image
import torch
from torchvision import models, transforms

# Load a pre-trained model
image_model = models.resnet50(pretrained=True)
image_model.eval()

# Image preprocessing
preprocess: Callable[[Image.Image], torch.Tensor] = transforms.Compose(
    [
        transforms.Resize(256),
        transforms.CenterCrop(224),
        transforms.ToTensor(),
    ]
)


def image_embed(image: Image.Image) -> List[float]:
    input_tensor: torch.Tensor = preprocess(image)
    input_batch = input_tensor.unsqueeze(0)  # Create a mini-batch
    with torch.no_grad():
        output = image_model(input_batch)
    return output.numpy().flatten()
