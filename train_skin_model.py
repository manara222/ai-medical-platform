import os
import copy
import torch
import torch.nn as nn
import torch.optim as optim

from torchvision import datasets, transforms, models
from torch.utils.data import DataLoader, WeightedRandomSampler
from collections import Counter

# =========================
# Paths
# =========================
TRAIN_DIR = "data/datasets/skin/train"
VAL_DIR = "data/datasets/skin/val"
MODEL_SAVE_PATH = "models/skin/weights/skin_model.pth"

# =========================
# Settings
# =========================
IMAGE_SIZE = 224
BATCH_SIZE = 16
NUM_EPOCHS = 20
LEARNING_RATE = 1e-4

DEVICE = torch.device("cuda" if torch.cuda.is_available() else "cpu")
print(f"Using device: {DEVICE}")

# =========================
# Transforms
# =========================
train_transforms = transforms.Compose([
    transforms.Resize((IMAGE_SIZE, IMAGE_SIZE)),
    transforms.RandomHorizontalFlip(),
    transforms.RandomRotation(15),
    transforms.ColorJitter(brightness=0.1, contrast=0.1),
    transforms.ToTensor(),
    transforms.Normalize([0.485, 0.456, 0.406],
                         [0.229, 0.224, 0.225])
])

val_transforms = transforms.Compose([
    transforms.Resize((IMAGE_SIZE, IMAGE_SIZE)),
    transforms.ToTensor(),
    transforms.Normalize([0.485, 0.456, 0.406],
                         [0.229, 0.224, 0.225])
])

# =========================
# Dataset
# =========================
train_dataset = datasets.ImageFolder(TRAIN_DIR, transform=train_transforms)
val_dataset = datasets.ImageFolder(VAL_DIR, transform=val_transforms)

class_names = train_dataset.classes
num_classes = len(class_names)

print("Classes:", class_names)
print("Train samples:", len(train_dataset))
print("Val samples:", len(val_dataset))

# =========================
# WeightedRandomSampler
# =========================
targets = train_dataset.targets
class_count = Counter(targets)

print("\nTrain class counts:")
for i, cls in enumerate(class_names):
    print(cls, ":", class_count[i])

class_weights = []
for i in range(num_classes):
    class_weights.append(1.0 / class_count[i])

sample_weights = [class_weights[t] for t in targets]
sample_weights = torch.DoubleTensor(sample_weights)

sampler = WeightedRandomSampler(
    weights=sample_weights,
    num_samples=len(sample_weights),
    replacement=True
)

train_loader = DataLoader(
    train_dataset,
    batch_size=BATCH_SIZE,
    sampler=sampler
)

val_loader = DataLoader(
    val_dataset,
    batch_size=BATCH_SIZE,
    shuffle=False
)

# =========================
# Model
# =========================
model = models.efficientnet_b0(
    weights=models.EfficientNet_B0_Weights.DEFAULT
)

for param in model.parameters():
    param.requires_grad = False

# نفك آخر بلوك
for param in model.features[-1].parameters():
    param.requires_grad = True

in_features = model.classifier[1].in_features
model.classifier[1] = nn.Linear(in_features, num_classes)

model = model.to(DEVICE)

# =========================
# Loss + Optimizer
# =========================
criterion = nn.CrossEntropyLoss()

optimizer = optim.Adam(
    filter(lambda p: p.requires_grad, model.parameters()),
    lr=LEARNING_RATE
)

scheduler = optim.lr_scheduler.ReduceLROnPlateau(
    optimizer,
    mode="min",
    factor=0.5,
    patience=2
)

# =========================
# Training
# =========================
best_val_acc = 0.0
best_model_wts = copy.deepcopy(model.state_dict())

for epoch in range(NUM_EPOCHS):

    print(f"\nEpoch {epoch+1}/{NUM_EPOCHS}")
    print("-" * 30)

    # ===== Train =====
    model.train()

    running_loss = 0.0
    running_corrects = 0
    total_train = 0

    for inputs, labels in train_loader:

        inputs = inputs.to(DEVICE)
        labels = labels.to(DEVICE)

        optimizer.zero_grad()

        outputs = model(inputs)
        _, preds = torch.max(outputs, 1)

        loss = criterion(outputs, labels)

        loss.backward()
        optimizer.step()

        running_loss += loss.item() * inputs.size(0)
        running_corrects += torch.sum(preds == labels.data)
        total_train += labels.size(0)

    train_loss = running_loss / total_train
    train_acc = running_corrects.double() / total_train

    # ===== Validation =====
    model.eval()

    running_loss = 0.0
    running_corrects = 0
    total_val = 0

    with torch.no_grad():
        for inputs, labels in val_loader:

            inputs = inputs.to(DEVICE)
            labels = labels.to(DEVICE)

            outputs = model(inputs)
            _, preds = torch.max(outputs, 1)

            loss = criterion(outputs, labels)

            running_loss += loss.item() * inputs.size(0)
            running_corrects += torch.sum(preds == labels.data)
            total_val += labels.size(0)

    val_loss = running_loss / total_val
    val_acc = running_corrects.double() / total_val

    scheduler.step(val_loss)

    print(f"Train Loss: {train_loss:.4f} | Train Acc: {train_acc:.4f}")
    print(f"Val Loss:   {val_loss:.4f} | Val Acc:   {val_acc:.4f}")

    if val_acc > best_val_acc:
        best_val_acc = val_acc
        best_model_wts = copy.deepcopy(model.state_dict())
        print("Best model updated.")

# =========================
# Save Model
# =========================
model.load_state_dict(best_model_wts)

os.makedirs(os.path.dirname(MODEL_SAVE_PATH), exist_ok=True)
torch.save(model.state_dict(), MODEL_SAVE_PATH)

print("\nTraining completed.")
print(f"Best Val Accuracy: {best_val_acc:.4f}")
print(f"Model saved to: {MODEL_SAVE_PATH}")