from __future__ import annotations
from torch.optim import Adam
import pickle

from sentineltools.images import load_image, thumbnail, convert_image_mode
from sentineltools.utils.progressbar import ProgressBar

from torch.utils.data import Dataset
import os
import torch.nn as nn
from typing import Union

from diffusers import AutoencoderKL
import torch

from PIL import Image
import numpy as np


class AutoVAE:
    def __init__(self, model_name="CompVis/stable-diffusion-v1-4", cache_dir="models\\pretrained\\autovae", device='cuda'):
        """
        Initializes the AutoVAE class by loading a pretrained VAE model.

        :param model_name: The name or path of the pretrained model to load
        :param cache_dir: Directory to cache the downloaded model
        :param device: Device to load the model on ('cuda' or 'cpu')
        """
        self.device = torch.device(device)
        self.vae = AutoencoderKL.from_pretrained(
            model_name,
            subfolder="vae",  # Correct subfolder inside the model repository
            cache_dir=cache_dir  # Directory where the model should be cached
        ).to(self.device)

    def encode(self, image: torch.Tensor) -> torch.Tensor:
        """
        Encodes an image into a latent embedding.

        :param image: Tensor of shape (batch_size, 3, height, width)
        :returns: Latent embedding tensor
        """
        image = image.to(self.device)
        with torch.no_grad():
            embedding = self.vae.encode(image).latent_dist.sample()
            embedding = embedding * self.vae.config.scaling_factor
        return embedding

    def decode(self, embedding: torch.Tensor) -> torch.Tensor:
        """
        Decodes a latent embedding back into an image.

        :param latents: Latent embedding tensor
        :returns: Decoded image tensor
        """
        embedding = embedding.to(self.device)
        embedding = embedding / self.vae.config.scaling_factor
        with torch.no_grad():
            image = self.vae.decode(embedding).sample
        return image

    def to_pil_image(self, tensor_image):
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

    def from_pil_image(self, pil_image: Union[Image.Image, list[Image.Image]]) -> torch.Tensor:
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


class NextFrameGeneratorDataset(Dataset):
    def __init__(self, model: NextFrameGenerator, folder_path: str):
        """
        Initializes the ClipDataset class.

        :param folder_path: path to the main folder containing clip folders (should contain folders with numbered images like car\\frame_001.png)
        :param model: An instance of the NextFrameGenerator model to preprocess images
        """
        self.folder_path = folder_path
        self.model = model
        self.data = []

        # Load and process all clip folders
        self._load_data()

    def _load_data(self):
        """
        Loads and processes images from clip folders into the dataset, with caching support.
        """
        clip_folders = [os.path.join(self.folder_path, d) for d in os.listdir(
            self.folder_path) if os.path.isdir(os.path.join(self.folder_path, d)) and not d.startswith("_")]

        total_images = 0
        new_clip_folder_data = []
        for folder_path in clip_folders:
            folder_name = os.path.basename(folder_path)
            folder_dirname = os.path.dirname(folder_path)
            cached_folder_name = folder_name + "_cached.pkl"
            cached_folder_path = os.path.join(
                folder_dirname, cached_folder_name)

            # Count total images for progress bar
            if os.path.exists(cached_folder_path):
                # If cache exists, load image count from cache
                with open(cached_folder_path, 'rb') as cache_file:
                    cached_data = pickle.load(cache_file)
                    total_images += len(cached_data)
            else:
                # If no cache, count the number of image files
                image_files = [f for f in os.listdir(
                    folder_path) if f.endswith('.jpg') or f.endswith('.png')]
                total_images += len(image_files)

            new_clip_folder_data.append(
                (folder_path, folder_name, cached_folder_path, cached_folder_name))

        clip_folders = new_clip_folder_data

        # Create progress bar with total number of images
        progressbar = ProgressBar(
            total_images, f"Clip Folders: [0/{len(clip_folders)}] Frame: [0/0]")

        for i, (folder_path, folder_name, cached_folder_path, cached_folder_name) in enumerate(clip_folders):
            if os.path.exists(cached_folder_path):
                # Load from cache
                with open(cached_folder_path, 'rb') as cache_file:
                    cached_data = pickle.load(cache_file)
                    # Load cached training examples
                    self.data.extend(cached_data)
                    for j in range(len(cached_data)):
                        progressbar.update(1)
            else:
                # Process new images and create training examples
                image_files = [f for f in os.listdir(
                    folder_path) if f.endswith('.jpg') or f.endswith('.png')]
                image_files = sorted(image_files, key=lambda x: int(
                    ''.join(filter(str.isdigit, os.path.splitext(x)[0]))))

                processed_images = []

                for j, image_file in enumerate(image_files):
                    image_path = os.path.join(folder_path, image_file)
                    pillow_image = load_image(image_path)
                    thumbnail_image = thumbnail(
                        convert_image_mode(pillow_image, "RGB"), size=(512, 512))
                    tensor_image = self.model.autovae.from_pil_image(
                        thumbnail_image)
                    tensor_emb = self.model.autovae.encode(tensor_image)
                    processed_images.append((tensor_emb, image_path))

                    progressbar.set_description(
                        f"Clip Folders: [{i + 1}/{len(clip_folders)}] Frame: [{j + 1}/{len(image_files)}]")
                    progressbar.update(1)

                # Create training examples with a sliding window of 16, offset by 1
                training_examples = []
                for start_idx in range(len(processed_images) - 16):
                    chunk = processed_images[start_idx:start_idx + 16]

                    if len(chunk) < 4:
                        continue  # Skip chunks with less than 4 examples

                    input_images = chunk[:-1]
                    target_image = chunk[-1]
                    training_examples.append((input_images, target_image))

                # Save training examples to cache
                with open(cached_folder_path, 'wb') as cache_file:
                    pickle.dump(training_examples, cache_file)

                # Add the training examples to the dataset
                self.data.extend(training_examples)

        progressbar.close()

    def __len__(self):
        return len(self.data)

    def __getitem__(self, idx) -> tuple[list[tuple[torch.Tensor, str]], tuple[torch.Tensor, str]]:
        """
        Returns an example from the dataset.

        :param idx: Index of the example to return
        :returns: Tuple of (list of tensors, target tensor)
        """
        return self.data[idx]


class ConvLSTMCell(nn.Module):
    def __init__(self, input_dim, hidden_dim, kernel_size):
        super(ConvLSTMCell, self).__init__()

        self.hidden_dim = hidden_dim
        self.conv = nn.Conv2d(in_channels=input_dim + hidden_dim,
                              out_channels=4 * hidden_dim,
                              kernel_size=kernel_size,
                              padding=kernel_size // 2)

    def forward(self, x: torch.Tensor, hidden_state: tuple[torch.Tensor, torch.Tensor]):
        h, c = hidden_state
        # concatenate along channel dimension

        combined = torch.cat([x, h], dim=1)
        conv_output = self.conv(combined)

        (cc_i, cc_f, cc_o, cc_g) = torch.split(
            conv_output, self.hidden_dim, dim=1)
        i = torch.sigmoid(cc_i)
        f = torch.sigmoid(cc_f)
        o = torch.sigmoid(cc_o)
        g = torch.tanh(cc_g)

        c_next = f * c + i * g
        h_next = o * torch.tanh(c_next)

        return h_next, c_next


class NextFrameGenerator(nn.Module):
    def __init__(self, input_dim=4, hidden_dim=128, kernel_size=3, num_layers=2, device="cuda"):
        super(NextFrameGenerator, self).__init__()

        self.device = torch.device(device)

        # ConvLSTM layers
        self.lstm_cells = nn.ModuleList([
            ConvLSTMCell(input_dim if i == 0 else hidden_dim,
                         hidden_dim, kernel_size)
            for i in range(num_layers)
        ]).to(self.device)

        # Final convolution layer to reduce hidden_dim to input_dim (4 channels)
        self.final_conv = nn.Conv2d(
            hidden_dim, input_dim, kernel_size=1).to(self.device)

    def forward(self, x: torch.Tensor, hidden_state):
        """
        Forward pass through the ConvLSTM.

        :param x: Input tensor of shape [batch_size, channels, height, width] or [channels, height, width]
        :param hidden_state: Tuple of (hidden_state, cell_state), or None to initialize hidden states
        :returns: Updated hidden state and cell state
        """
        # Ensure the input tensor is batched, i.e., has the shape [batch_size, channels, height, width]
        if x.dim() == 3:  # If input is [channels, height, width]
            # Add a batch dimension: [1, channels, height, width]
            x = x.unsqueeze(0)

        batch_size, _, height, width = x.size()

        # If hidden_state is None, initialize it with zeros
        if hidden_state is None:
            h = [torch.zeros(batch_size, cell.hidden_dim, height, width, device=x.device)
                 for cell in self.lstm_cells]
            c = [torch.zeros(batch_size, cell.hidden_dim, height, width, device=x.device)
                 for cell in self.lstm_cells]
        else:
            h, c = hidden_state

        # Ensure hidden and cell states have the correct batch size
        if h[0].size(0) != batch_size:
            h = [torch.zeros(batch_size, cell.hidden_dim, height, width, device=x.device)
                 for cell in self.lstm_cells]
            c = [torch.zeros(batch_size, cell.hidden_dim, height, width, device=x.device)
                 for cell in self.lstm_cells]

        # Pass through each ConvLSTM cell
        next_h, next_c = [], []
        for i, lstm_cell in enumerate(self.lstm_cells):
            # Update hidden and cell states
            h[i], c[i] = lstm_cell(x, (h[i], c[i]))
            x = h[i]  # Output of current cell becomes input to the next
            next_h.append(h[i])
            next_c.append(c[i])

        # Final convolution to reduce hidden_dim to input_dim (e.g., 64 -> 4)
        output = self.final_conv(x)

        return output, (next_h, next_c)

    def next(self, input_data, hidden_state=None):
        """
        Takes an embedding or list of embeddings and returns the predicted next embedding.

        :param input_data: Either a single embedding tensor or a list of embedding tensors
        :returns: Predicted next embedding tensor
        """
        # Ensure the input is a list of embeddings (if not, convert it to a list)
        if isinstance(input_data, torch.Tensor):
            input_data = [input_data]

        # Process each embedding in the list
        for embedding in input_data:
            # If the input is [channels, height, width], add batch dim
            if embedding.dim() == 3:
                embedding = embedding.unsqueeze(0)

            # Forward pass for each embedding, updating the hidden state
            hidden_state = self(embedding, hidden_state)

        # The final prediction is the output from the last embedding in the sequence
        output, _ = hidden_state

        return output, hidden_state  # Return the final predicted next embedding

    def train_model(self, dataset: NextFrameGeneratorDataset, iterations: int = 10, learning_rate: float = 0.001):
        """
        Train the ConvLSTM model using the provided dataset.

        :param dataset: Dataset of sequences and expected next-frame embeddings
        :param iterations: Number of training epochs
        :param learning_rate: Learning rate for optimizer
        """
        self.train()  # Set model to training mode
        optimizer = Adam(self.parameters(), lr=learning_rate)
        criterion = nn.MSELoss()

        # Progress bar using the previously defined ProgressBar class
        progressbar = ProgressBar(
            iterations * len(dataset),
            f"Epoch: [0/{iterations}] Step: [0/{len(dataset)}] Loss: [0]"
        )

        for epoch in range(iterations):
            total_loss = 0.0

            for dataset_iter, (inputs, target) in enumerate(dataset):
                # Reset gradients and hidden states before processing each new sequence
                optimizer.zero_grad()

                # Initialize hidden and cell states to None
                hidden_state = None

                target_tensor, _ = target  # Extract target embedding tensor
                target_tensor = target_tensor.to(self.device)

                # Process input frames (embedding sequence) one by one
                for input_tensor, _ in inputs:
                    input_tensor = input_tensor.to(self.device)

                    # Forward pass through ConvLSTM cell by cell
                    hidden_state = self(input_tensor, hidden_state)

                # Predict the next frame embedding
                output, _ = hidden_state

                # Compute loss between predicted and true next embedding
                loss = criterion(output, target_tensor)
                total_loss += loss.item()

                # Backpropagation and optimization
                loss.backward()
                optimizer.step()

                # Update progress bar
                progressbar.update(1)
                progressbar.set_description(
                    f"Epoch: [{epoch+1}/{iterations}] Step: [{dataset_iter +
                                                              1}/{len(dataset)}] Loss: [{total_loss / (dataset_iter + 1):.4f}]"
                )

        progressbar.close()
