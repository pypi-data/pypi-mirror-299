from typing import Union
import torch
from PIL import Image
import numpy as np


def to_pil_image(tensor_image: torch.Tensor) -> list[Image.Image]:
    """
    Converts a tensor image or batch of tensor images to a PIL image or a list of PIL images.

    :param tensor_image: Tensor of shape (batch_size, 3, height, width) or (3, height, width)
    :returns: A PIL image or a list of PIL images
    """
    # Handle batched input
    if tensor_image.dim() == 4:
        images = []
        for img in tensor_image:
            img = img.squeeze(0).permute(1, 2, 0).detach().cpu().numpy()
            img = (img - img.min()) / (img.max() - img.min())
            img = (img * 255).astype(np.uint8)
            images.append(Image.fromarray(img))
        return images
    elif tensor_image.dim() == 3:
        img = tensor_image.permute(1, 2, 0).detach().cpu().numpy()
        img = (img - img.min()) / (img.max() - img.min())
        img = (img * 255).astype(np.uint8)
        return [Image.fromarray(img)]
    else:
        raise ValueError(
            "Unsupported tensor dimension. Expected 3 or 4 dimensions.")


def from_pil_image(pil_image: Union[Image.Image, list[Image.Image]]) -> torch.Tensor:
    """
    Converts a PIL image or a list of PIL images into a batched tensor.

    :param pil_image: A single PIL Image or a list of PIL Images
    :returns: A tensor of shape (batch_size, 3, height, width)
    """
    if isinstance(pil_image, list):
        tensors = []
        for img in pil_image:
            img_tensor = torch.from_numpy(
                np.array(img).astype(np.float32) / 255.0)
            # Change shape to (3, height, width)
            img_tensor = img_tensor.permute(2, 0, 1)
            tensors.append(img_tensor)
        batched_tensor = torch.stack(tensors)  # Combine into a batch
    else:
        img_tensor = torch.from_numpy(
            np.array(pil_image).astype(np.float32) / 255.0)
        # Change shape to (3, height, width)
        img_tensor = img_tensor.permute(2, 0, 1)
        batched_tensor = img_tensor.unsqueeze(0)  # Add a batch dimension

    return batched_tensor
