from pydantic import BaseModel

class PredictionResponse(BaseModel):
    disease_type: str
    predicted_class: str
    confidence: float
    report_message: str
    heatmap_path: str | None = None