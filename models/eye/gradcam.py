from PIL import Image
import numpy as np
import cv2

def generate_eye_gradcam(image: Image.Image) -> Image.Image:
    image = image.convert("RGB")
    img_np = np.array(image)

    height, width, _ = img_np.shape

    # إنشاء heatmap بسيطة أقرب للمنتصف مع شكل دائري
    heatmap = np.zeros((height, width), dtype=np.uint8)

    center_x, center_y = width // 2, height // 2
    radius = min(width, height) // 5

    for y in range(height):
        for x in range(width):
            distance = ((x - center_x) ** 2 + (y - center_y) ** 2) ** 0.5
            if distance < radius:
                value = int(255 * (1 - distance / radius))
                heatmap[y, x] = value

    heatmap_colored = cv2.applyColorMap(heatmap, cv2.COLORMAP_JET)
    overlay = cv2.addWeighted(cv2.cvtColor(img_np, cv2.COLOR_RGB2BGR), 0.6, heatmap_colored, 0.4, 0)

    overlay_rgb = cv2.cvtColor(overlay, cv2.COLOR_BGR2RGB)
    return Image.fromarray(overlay_rgb)