from PIL import Image
import numpy as np
import cv2

def preprocess_image(image: Image.Image, size=(224, 224)):
    # تحويل الصورة إلى RGB
    image = image.convert("RGB")

    # تغيير الحجم
    image = image.resize(size)

    # تحويل الصورة إلى numpy array
    img_np = np.array(image)

    # OpenCV بيشتغل غالبًا بصيغة BGR
    img_bgr = cv2.cvtColor(img_np, cv2.COLOR_RGB2BGR)

    # تقليل التشويش
    img_denoised = cv2.fastNlMeansDenoisingColored(img_bgr, None, 10, 10, 7, 21)

    # تحسين التباين بشكل بسيط باستخدام LAB + CLAHE
    lab = cv2.cvtColor(img_denoised, cv2.COLOR_BGR2LAB)
    l, a, b = cv2.split(lab)

    clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8, 8))
    l_enhanced = clahe.apply(l)

    lab_enhanced = cv2.merge((l_enhanced, a, b))
    img_enhanced = cv2.cvtColor(lab_enhanced, cv2.COLOR_LAB2RGB)

    # إرجاع الصورة كـ PIL Image
    return Image.fromarray(img_enhanced)