import torch
from torchvision import transforms
from PIL import Image
import io

def get_transform():
    """Returns the standard image transformation pipeline."""
    return transforms.Compose([
        transforms.Grayscale(num_output_channels=1),
        transforms.Resize((224, 224)),
        transforms.ToTensor(),
        transforms.Normalize((0.5,), (0.5,))
    ])

def preprocess_image(image_bytes):
    """Converts image bytes into a torch tensor ready for model inference."""
    try:
        image = Image.open(io.BytesIO(image_bytes)).convert('L')
        transform = get_transform()
        return transform(image).unsqueeze(0) # Add batch dimension
    except Exception as e:
        print(f"Preprocessing error: {e}")
        return None

def extract_metadata_features(case):
    """
    Extracts numerical features from Case model for multi-modal prediction.
    Currently returns a mock tensor as placeholder for tabular data integration.
    """
    # This could extract age, BMI, smoking status from 'case' object
    # and convert them to normalized numerical values.
    return torch.tensor([0.5, 0.2, 0.8]) # Mock features
