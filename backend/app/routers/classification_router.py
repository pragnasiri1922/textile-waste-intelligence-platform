from fastapi import APIRouter, Depends, File, HTTPException, UploadFile
from sqlalchemy.orm import Session

from backend.app import auth, models, schemas
from backend.app.database import get_db
from backend.app.services.classification_engine import (
    classify_material,
    preprocess_textile_image,
    simulate_image_analysis,
)
from backend.app.services.recyclability_engine import assess_recyclability
from backend.app.services.report_generator import (
    generate_batch_report,
    generate_summary_report,
)
from backend.app.services.waste_categorizer import (
    categorize_waste,
    get_disposal_recommendation,
)

router = APIRouter(prefix="/classify", tags=["Classification & Analysis"])


@router.post("/material")
async def analyze_textile(file: UploadFile = File(...)):
    if not file.content_type.startswith("image/"):
        raise HTTPException(
            status_code=400, detail="Uploaded file must be a valid image format."
        )

    file_bytes = await file.read()
    processed_image = preprocess_textile_image(file_bytes)
    result = classify_material(processed_image)

    return {"status": "success", "analysis": result}