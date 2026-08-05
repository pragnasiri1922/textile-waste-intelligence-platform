from fastapi import APIRouter, Depends, HTTPException, UploadFile, File
from sqlalchemy.orm import Session

from backend.app import schemas, models, auth
from backend.app.database import get_db
from backend.app.services.classification_engine import classify_material, simulate_image_analysis
from backend.app.services.waste_categorizer import categorize_waste, get_disposal_recommendation
from backend.app.services.recyclability_engine import assess_recyclability
from backend.app.services.report_generator import generate_batch_report, generate_summary_report

router = APIRouter(prefix="/api/classify", tags=["Classification & Analysis"])