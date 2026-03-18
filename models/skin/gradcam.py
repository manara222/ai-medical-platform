import torch
import cv2
import numpy as np
from PIL import Image
from torchvision import transforms

from models.skin.classifier import SkinClassifier
from app.config import SKIN_MODEL_PATH, SKIN_CLASSES, IMAGE_SIZE

device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

model_wrapper = SkinClassifier(SKIN_MODEL_PATH, SKIN_CLASSES)
model = model_wrapper.model

target_layer = model.features[-1]

transform = transforms.Compose([
    transforms.Resize(IMAGE_SIZE),
    transforms.ToTensor(),
])

def generate_skin_gradcam(image: Image.Image):
    model.eval()

    img = transform(image).unsqueeze(0).to(device)

    gradients = []
    activations = []

    def backward_hook(module, grad_in, grad_out):
        gradients.append(grad_out[0])

    def forward_hook(module, input, output):
        activations.append(output)

    forward_handle = target_layer.register_forward_hook(forward_hook)
    backward_handle = target_layer.register_backward_hook(backward_hook)

    output = model(img)
    pred_class = output.argmax(dim=1)

    model.zero_grad()
    output[0, pred_class].backward()

    grads = gradients[0].cpu().data.numpy()[0]
    acts = activations[0].cpu().data.numpy()[0]

    weights = np.mean(grads, axis=(1, 2))

    cam = np.zeros(acts.shape[1:], dtype=np.float32)
    for i, w in enumerate(weights):
        cam += w * acts[i]

    cam = np.maximum(cam, 0)

    if cam.max() != 0:
        cam = cam / cam.max()

    cam_resized = cv2.resize(cam, (image.size[0], image.size[1]))

    heatmap = cv2.applyColorMap(np.uint8(255 * cam_resized), cv2.COLORMAP_JET)

    img_np = np.array(image)
    img_bgr = cv2.cvtColor(img_np, cv2.COLOR_RGB2BGR)

    overlay = cv2.addWeighted(img_bgr, 0.6, heatmap, 0.4, 0)

    # ===== Smart Localization Box =====
    heatmap_gray = np.uint8(255 * cam_resized)
    _, thresh = cv2.threshold(heatmap_gray, 150, 255, cv2.THRESH_BINARY)

    contours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    if contours:
        c = max(contours, key=cv2.contourArea)
        x, y, w, h = cv2.boundingRect(c)
        cv2.rectangle(overlay, (x, y), (x + w, y + h), (0, 255, 0), 3)
        cv2.putText(
            overlay,
            "Suspicious Region",
            (x, max(y - 10, 20)),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.6,
            (0, 255, 0),
            2,
            cv2.LINE_AA
        )

    overlay_rgb = cv2.cvtColor(overlay, cv2.COLOR_BGR2RGB)

    forward_handle.remove()
    backward_handle.remove()

    return Image.fromarray(overlay_rgb)