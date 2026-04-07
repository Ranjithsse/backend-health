import torch
import torch.nn as nn
import torch.nn.functional as F

class HealthPredictCNN(nn.Module):
    """
    A multi-output CNN for medical image analysis and risk prediction.
    Processes an input image (X-ray/Scan) and outputs multiple clinical metrics.
    """
    def __init__(self):
        super(HealthPredictCNN, self).__init__()
        
        # Convolutional layers for image feature extraction
        self.conv1 = nn.Conv2d(1, 32, kernel_size=3, padding=1)
        self.conv2 = nn.Conv2d(32, 64, kernel_size=3, padding=1)
        self.conv3 = nn.Conv2d(64, 128, kernel_size=3, padding=1)
        self.pool = nn.MaxPool2d(2, 2)
        
        # Fully connected layers for shared representation
        self.fc_shared = nn.Linear(128 * 28 * 28, 512) 
        
        # Output Heads
        # 1. Risk Score (Regression: 0-100)
        self.fc_risk_score = nn.Linear(512, 1)
        
        # 2. Risk Level (Classification: Low, Moderate, High, Critical)
        self.fc_risk_level = nn.Linear(512, 4)
        
        # 3. Long Term Prediction (3 nodes for 1yr, 3yr, 5yr probabilities)
        self.fc_long_term = nn.Linear(512, 3)
        
        # 4. Risk Factors (Multi-label classification for key indicators)
        self.fc_risk_factors = nn.Linear(512, 6) # e.g., Smoking, BP, BMI, etc.

    def forward(self, x):
        # Image Feature Extraction
        x = self.pool(F.relu(self.conv1(x)))
        x = self.pool(F.relu(self.conv2(x)))
        x = self.pool(F.relu(self.conv3(x)))
        
        x = x.view(-1, 128 * 28 * 28)
        shared = F.relu(self.fc_shared(x))
        
        # Head-specific outputs
        risk_score = torch.sigmoid(self.fc_risk_score(shared)) * 100
        risk_level = self.fc_risk_level(shared) # Logits
        long_term = torch.sigmoid(self.fc_long_term(shared)) # Probabilities
        risk_factors = torch.sigmoid(self.fc_risk_factors(shared)) # Probabilities
        
        return {
            'risk_score': risk_score,
            'risk_level': risk_level,
            'long_term': long_term,
            'risk_factors': risk_factors
        }
