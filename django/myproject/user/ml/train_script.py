import torch
import torch.nn as nn
import torch.optim as optim
from torch.utils.data import DataLoader, Dataset
from .model import HealthPredictCNN
import os

class MockMedicalDataset(Dataset):
    """
    Constructs a synthetic dataset for demonstration and testing of the training script.
    In a real scenario, this would load X-ray images from a filesystem.
    """
    def __init__(self, size=100):
        self.size = size

    def __len__(self):
        return self.size

    def __getitem__(self, idx):
        # Image (1, 224, 224)
        image = torch.randn(1, 224, 224)
        
        # Labels
        risk_score = torch.tensor([50.0]) # Target risk score
        risk_level = torch.tensor(1) # Target index (Low, Moderate, High, Critical)
        long_term = torch.tensor([20.0, 40.0, 60.0]) # 1y, 3y, 5y
        risk_factors = torch.tensor([1.0, 0.0, 1.0, 0.0, 0.0, 0.0]) # Binary labels
        
        return image, {
            'risk_score': risk_score,
            'risk_level': risk_level,
            'long_term': long_term,
            'risk_factors': risk_factors
        }

def train_model(data_dir=None, epochs=5, save_path="health_predict_model.pth"):
    """
    Trains the HealthPredictCNN on available data.
    """
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    model = HealthPredictCNN().to(device)
    optimizer = optim.Adam(model.parameters(), lr=0.001)
    
    # Loss functions
    mse_loss = nn.MSELoss()
    ce_loss = nn.CrossEntropyLoss()
    bce_loss = nn.BCELoss()
    
    # Dataset setup
    dataset = MockMedicalDataset(size=200) # Replace with real dataset loader
    dataloader = DataLoader(dataset, batch_size=16, shuffle=True)
    
    print(f"Starting training on {device}...")
    
    for epoch in range(epochs):
        model.train()
        total_loss = 0
        for batch_idx, (images, targets) in enumerate(dataloader):
            images = images.to(device)
            optimizer.zero_grad()
            
            outputs = model(images)
            
            # Combine losses from all heads
            loss_score = mse_loss(outputs['risk_score'], targets['risk_score'].to(device))
            loss_level = ce_loss(outputs['risk_level'], targets['risk_level'].to(device))
            loss_long = mse_loss(outputs['long_term'], targets['long_term'].to(device) / 100.0)
            loss_factors = bce_loss(outputs['risk_factors'], targets['risk_factors'].to(device))
            
            loss = loss_score + loss_level + loss_long + loss_factors
            loss.backward()
            optimizer.step()
            
            total_loss += loss.item()
            
        print(f"Epoch {epoch+1}/{epochs}, Loss: {total_loss/len(dataloader):.4f}")
        
    torch.save(model.state_dict(), save_path)
    print(f"Model saved to {save_path}")

if __name__ == "__main__":
    # Ensure this runs as a script for the user
    train_model(epochs=3)
