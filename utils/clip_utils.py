import torch
import clip
import numpy as np
from PIL import Image
import torchvision.transforms as transforms
from config import Config

class ClipModel:
    _instance = None
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(ClipModel, cls).__new__(cls)
            cls._instance.device = "cuda" if torch.cuda.is_available() else "cpu"
            cls._instance.model, cls._instance.preprocess = clip.load(Config.CLIP_MODEL, cls._instance.device)
            cls._instance.model.eval()
            
            # Define the transform
            cls._instance.transform = transforms.Compose([
                transforms.Resize((224, 224)),
                transforms.ToTensor(),
                transforms.Normalize(
                    mean=[0.48145466, 0.4578275, 0.40821073],
                    std=[0.26862954, 0.26130258, 0.27577711]
                )
            ])
        
        return cls._instance
    
    def encode_image(self, image):
        """
        Encode an image using CLIP.
        
        Args:
            image: PIL Image or path to image
            
        Returns:
            numpy array: Image embedding
        """
        if isinstance(image, str):
            # It's a file path
            image = Image.open(image).convert("RGB")
        
        # Apply the transform
        image_tensor = self.transform(image).unsqueeze(0).to(self.device)
        
        with torch.no_grad():
            image_emb = self.model.encode_image(image_tensor).cpu().numpy().flatten()
        
        return image_emb
    
    def encode_text(self, text):
        """
        Encode text using CLIP.
        
        Args:
            text: String text to encode
            
        Returns:
            numpy array: Text embedding
        """
        text_tokens = clip.tokenize([text]).to(self.device)
        
        with torch.no_grad():
            text_emb = self.model.encode_text(text_tokens).cpu().numpy().flatten()
        
        return text_emb
    
    def get_device(self):
        """Get the device being used (CPU or CUDA)"""
        return self.device

