from PIL import Image
import numpy as np
import cv2

def generate_heatmap_only(image: Image.Image) -> Image.Image:
    image = image.convert("RGB")
    img_np = np.array(image)

    heatmap = np.zeros((img_np.shape[0], img_np.shape[1]), dtype=np.uint8)

    center_x, center_y = img_np.shape[1] // 2, img_np.shape[0] // 2
    radius = min(img_np.shape[0], img_np.shape[1]) // 3

    for y in range(img_np.shape[0]):
        for x in range(img_np.shape[1]):
            dist = ((x - center_x) ** 2 + (y - center_y) ** 2) ** 0.5
            if dist < radius:
                heatmap[y, x] = int(255 * (1 - dist / radius))

    heatmap_colored = cv2.applyColorMap(heatmap, cv2.COLORMAP_JET)
    overlay = cv2.addWeighted(cv2.cvtColor(img_np, cv2.COLOR_RGB2BGR), 0.6, heatmap_colored, 0.4, 0)

    overlay_rgb = cv2.cvtColor(overlay, cv2.COLOR_BGR2RGB)
    return Image.fromarray(overlay_rgb)