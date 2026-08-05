from fastapi import APIRouter, Depends, UploadFile, File, HTTPException
from sqlalchemy.orm import Session
import csv
import io

from backend.app import schemas, models, auth
from backend.app.database import get_db
router = APIRouter(prefix="/api/upload", tags=["Data Upload"])

@router.post("/csv")
async def upload_csv(
    file: UploadFile = File(...),
    db: Session = Depends(get_db),
    current_user: models.User = Depends(auth.get_current_user)
):
    if not file.filename.endswith('.csv'):
        raise HTTPException(status_code=400, detail="File must be a CSV")
    
    contents = await file.read()
    try:
        csv_reader = csv.DictReader(io.StringIO(contents.decode('utf-8')))
        imported_count = 0
        for row in csv_reader:
            # Map CSV columns to model attributes. Assume basic mapping or fallback.
            try:
                batch = models.WasteBatch(
                    batch_id=row.get("batch_id"),
                    fabric_type=row.get("fabric_type"),
                    source=row.get("source"),
                    quantity_kg=float(row.get("quantity_kg", 0)),
                    color=row.get("color"),
                    condition=row.get("condition"),
                    waste_category=row.get("waste_category"),
                    recyclability_score=float(row.get("recyclability_score", 0)),
                    contamination_level=row.get("contamination_level", "None"),
                    damage_level=row.get("damage_level", "None"),
                    notes=row.get("notes"),
                    user_id=current_user.id
                )
                db.add(batch)
                imported_count += 1
            except Exception as e:
                # Skip invalid rows or handle properly
                pass
        db.commit()
        return {"detail": f"Successfully imported {imported_count} records"}
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=400, detail=f"Error processing file: {str(e)}")
