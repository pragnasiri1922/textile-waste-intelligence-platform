from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.responses import StreamingResponse
from sqlalchemy.orm import Session
from typing import List, Optional
import csv
import io
import schemas, models, auth
from database import get_db

router = APIRouter(prefix="/api/inventory", tags=["Inventory"])

@router.get("/", response_model=List[schemas.WasteBatchResponse])
def get_batches(
    fabric_type: Optional[str] = None,
    condition: Optional[str] = None,
    waste_category: Optional[str] = None,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(auth.get_current_user)
):
    query = db.query(models.WasteBatch)
    if fabric_type:
        query = query.filter(models.WasteBatch.fabric_type == fabric_type)
    if condition:
        query = query.filter(models.WasteBatch.condition == condition)
    if waste_category:
        query = query.filter(models.WasteBatch.waste_category == waste_category)
    return query.all()

@router.post("/", response_model=schemas.WasteBatchResponse)
def create_batch(
    batch: schemas.WasteBatchCreate,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(auth.get_current_user)
):
    db_batch = db.query(models.WasteBatch).filter(models.WasteBatch.batch_id == batch.batch_id).first()
    if db_batch:
        raise HTTPException(status_code=400, detail="Batch ID already exists")
    
    new_batch = models.WasteBatch(**batch.model_dump(), user_id=current_user.id)
    db.add(new_batch)
    db.commit()
    db.refresh(new_batch)
    return new_batch

@router.get("/export/csv")
def export_csv(
    db: Session = Depends(get_db),
    current_user: models.User = Depends(auth.get_current_user)
):
    batches = db.query(models.WasteBatch).all()
    output = io.StringIO()
    writer = csv.writer(output)
    writer.writerow([
        "ID", "Batch ID", "Fabric Type", "Source", "Quantity (kg)", 
        "Color", "Condition", "Waste Category", "Recyclability Score", 
        "Contamination Level", "Damage Level", "Notes", "Created At"
    ])
    for b in batches:
        writer.writerow([
            b.id, b.batch_id, b.fabric_type, b.source, b.quantity_kg,
            b.color, b.condition, b.waste_category, b.recyclability_score,
            b.contamination_level, b.damage_level, b.notes, b.created_at
        ])
    
    output.seek(0)
    return StreamingResponse(
        iter([output.getvalue()]), 
        media_type="text/csv", 
        headers={"Content-Disposition": "attachment; filename=inventory.csv"}
    )

@router.get("/{batch_id}", response_model=schemas.WasteBatchResponse)
def get_batch(
    batch_id: int,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(auth.get_current_user)
):
    batch = db.query(models.WasteBatch).filter(models.WasteBatch.id == batch_id).first()
    if not batch:
        raise HTTPException(status_code=404, detail="Batch not found")
    return batch

@router.put("/{batch_id}", response_model=schemas.WasteBatchResponse)
def update_batch(
    batch_id: int,
    batch_update: schemas.WasteBatchCreate,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(auth.get_current_user)
):
    db_batch = db.query(models.WasteBatch).filter(models.WasteBatch.id == batch_id).first()
    if not db_batch:
        raise HTTPException(status_code=404, detail="Batch not found")
    
    for key, value in batch_update.model_dump().items():
        setattr(db_batch, key, value)
    
    db.commit()
    db.refresh(db_batch)
    return db_batch

@router.delete("/{batch_id}")
def delete_batch(
    batch_id: int,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(auth.get_current_user)
):
    db_batch = db.query(models.WasteBatch).filter(models.WasteBatch.id == batch_id).first()
    if not db_batch:
        raise HTTPException(status_code=404, detail="Batch not found")
    
    db.delete(db_batch)
    db.commit()
    return {"detail": "Batch deleted successfully"}
