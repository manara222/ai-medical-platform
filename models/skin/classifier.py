import os
from PIL import Image
import torch
import torch.nn as nn
from torchvision import models, transforms

from app.config import IMAGE_SIZE, USE_REAL_MODELS

class SkinClassifier:
    def __init__(self, model_path: str, class_names: list[str]):
        self.model_path = model_path
        self.class_names = class_names
        self.device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
        self.use_real_model = False

        self.transform = transforms.Compose([
            transforms.Resize(IMAGE_SIZE),
            transforms.ToTensor(),
        ])

        if USE_REAL_MODELS and os.path.exists(self.model_path):
            try:
                self.model = models.efficientnet_b0(weights=None)
                in_features = self.model.classifier[1].in_features
                self.model.classifier[1] = nn.Linear(in_features, len(self.class_names))

                state_dict = torch.load(self.model_path, map_location=self.device)
                self.model.load_state_dict(state_dict)

                self.model.to(self.device)
                self.model.eval()
                self.use_real_model = True

                print("Skin model loaded successfully.")
            except Exception as e:
                print(f"Could not load real skin model: {e}")
                self.model = None
        else:
            self.model = None
            print("Skin model weights not found. Using mock prediction.")

    def predict(self, image: Image.Image):
        if self.use_real_model and self.model is not None:
            image_tensor = self.transform(image).unsqueeze(0).to(self.device)

            with torch.no_grad():
                outputs = self.model(image_tensor)
                probs = torch.softmax(outputs, dim=1)
                confidence, pred_class = torch.max(probs, dim=1)

            return {
                "predicted_class": self.class_names[pred_class.item()],
                "confidence": float(confidence.item())
            }

        return {
            "predicted_class": self.class_names[0],
            "confidence": 0.91
        }