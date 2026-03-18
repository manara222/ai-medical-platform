SKIN_MODEL_PATH = "models/skin/weights/skin_model.pth"
EYE_MODEL_PATH = "models/eye/weights/eye_model.pth"
COVID_MODEL_PATH = "models/covid/weights/covid_model.pth"
BREAST_MODEL_PATH = "models/breast/weights/breast_model.pth"

IMAGE_SIZE = (224, 224)

SKIN_CLASSES = [
    "akiec",
    "bcc",
    "bkl",
    "df",
    "mel",
    "nv",
    "vasc"
]

EYE_CLASSES = [
    "Cataract",
    "Diabetic_Retinopathy",
    "Glaucoma",
    "Normal"
]

COVID_CLASSES = [
    "Covid",
    "Normal",
    "Viral Pneumonia"
]

BREAST_CLASSES = [
    "benign",
    "malignant",
    "normal"
]

USE_REAL_MODELS = True