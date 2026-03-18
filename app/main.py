from fastapi import FastAPI, UploadFile, File, Form
from fastapi.responses import StreamingResponse, JSONResponse
from PIL import Image
import io
import os

from app.config import (
    SKIN_MODEL_PATH,
    EYE_MODEL_PATH,
    COVID_MODEL_PATH,
    BREAST_MODEL_PATH,
    SKIN_CLASSES,
    EYE_CLASSES,
    COVID_CLASSES,
    BREAST_CLASSES,
)
from utils.image_preprocessing import preprocess_image
from utils.report_generator import generate_pdf_report
from utils.clinical_recommendations import get_clinical_recommendation
from utils.risk_helper import get_risk_info

from models.skin.classifier import SkinClassifier
from models.eye.classifier import EyeClassifier
from models.covid.classifier import CovidClassifier
from models.breast.classifier import BreastClassifier

from models.skin.gradcam import generate_skin_gradcam

app = FastAPI(title="AI Multi-Disease Diagnosis Platform")

skin_model = SkinClassifier(SKIN_MODEL_PATH, SKIN_CLASSES)
eye_model = EyeClassifier(EYE_MODEL_PATH, EYE_CLASSES)
covid_model = CovidClassifier(COVID_MODEL_PATH, COVID_CLASSES)
breast_model = BreastClassifier(BREAST_MODEL_PATH, BREAST_CLASSES)

OUTPUT_DIR = "data/outputs"
os.makedirs(OUTPUT_DIR, exist_ok=True)


@app.get("/")
def root():
    return {"message": "API is running"}


@app.post("/analyze")
async def analyze_image(image_type: str = Form(...), file: UploadFile = File(...)):
    contents = await file.read()
    image = Image.open(io.BytesIO(contents)).convert("RGB")

    processed_image = preprocess_image(image)
    normalized_type = image_type.strip().lower()

    if normalized_type == "skin":
        result = skin_model.predict(processed_image)
        disease_type = "Skin Disease"

    elif normalized_type == "eye":
        result = eye_model.predict(processed_image)
        disease_type = "Eye Disease"

    elif normalized_type == "covid":
        result = covid_model.predict(processed_image)
        disease_type = "COVID-19"

    elif normalized_type == "breast":
        result = breast_model.predict(processed_image)
        disease_type = "Breast Cancer"

    else:
        return JSONResponse(
            status_code=400,
            content={"error": "Invalid image_type. Use 'skin', 'eye', 'covid', or 'breast'."}
        )

    recommendation = get_clinical_recommendation(result["predicted_class"])
    risk_info = get_risk_info(
        disease_type,
        result["predicted_class"],
        result["confidence"]
    )

    return {
        "disease_type": disease_type,
        "predicted_class": result["predicted_class"],
        "confidence": result["confidence"],
        "clinical_insight": recommendation["clinical_insight"],
        "next_step": recommendation["next_step"],
        "risk_level": risk_info["risk_level"],
        "urgency": risk_info["urgency"],
        "risk_color": risk_info["color"]
    }


@app.post("/preprocess")
async def preprocess_uploaded_image(file: UploadFile = File(...)):
    contents = await file.read()
    image = Image.open(io.BytesIO(contents)).convert("RGB")

    processed_image = preprocess_image(image)

    img_bytes = io.BytesIO()
    processed_image.save(img_bytes, format="PNG")
    img_bytes.seek(0)

    return StreamingResponse(img_bytes, media_type="image/png")


@app.post("/gradcam")
async def generate_gradcam(image_type: str = Form(...), file: UploadFile = File(...)):
    try:
        normalized_type = image_type.strip().lower()

        if normalized_type != "skin":
            return JSONResponse(
                status_code=400,
                content={
                    "error": "Explainability is currently available for skin analysis only."
                }
            )

        contents = await file.read()
        image = Image.open(io.BytesIO(contents)).convert("RGB")
        processed_image = preprocess_image(image)

        gradcam_image = generate_skin_gradcam(processed_image)

        img_bytes = io.BytesIO()
        gradcam_image.save(img_bytes, format="PNG")
        img_bytes.seek(0)

        return StreamingResponse(img_bytes, media_type="image/png")

    except Exception as e:
        return JSONResponse(
            status_code=500,
            content={"error": f"Grad-CAM generation failed: {str(e)}"}
        )


@app.post("/report")
async def generate_report(image_type: str = Form(...), file: UploadFile = File(...)):
    contents = await file.read()
    image = Image.open(io.BytesIO(contents)).convert("RGB")

    processed_image = preprocess_image(image)
    normalized_type = image_type.strip().lower()

    if normalized_type == "skin":
        result = skin_model.predict(processed_image)
        disease_type = "Skin Disease"

    elif normalized_type == "eye":
        result = eye_model.predict(processed_image)
        disease_type = "Eye Disease"

    elif normalized_type == "covid":
        result = covid_model.predict(processed_image)
        disease_type = "COVID-19"

    elif normalized_type == "breast":
        result = breast_model.predict(processed_image)
        disease_type = "Breast Cancer"

    else:
        return JSONResponse(
            status_code=400,
            content={"error": "Invalid image_type. Use 'skin', 'eye', 'covid', or 'breast'."}
        )

    image_path = os.path.join(OUTPUT_DIR, "report_input.png")
    pdf_path = os.path.join(OUTPUT_DIR, "medical_report.pdf")

    processed_image.save(image_path)

    generate_pdf_report(
        output_path=pdf_path,
        image_path=image_path,
        disease_type=disease_type,
        predicted_class=result["predicted_class"],
        confidence=result["confidence"]
    )

    with open(pdf_path, "rb") as f:
        pdf_bytes = io.BytesIO(f.read())

    pdf_bytes.seek(0)
    return StreamingResponse(pdf_bytes, media_type="application/pdf")