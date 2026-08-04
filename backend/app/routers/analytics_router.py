from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from sqlalchemy import func
import schemas, models
from database import get_db

router = APIRouter(prefix="/api/analytics", tags=["Analytics"])

@router.get("/summary", response_model=schemas.AnalyticsResponse)
def get_summary(db: Session = Depends(get_db)):
    total_batches = db.query(models.WasteBatch).count()
    total_weight = db.query(func.sum(models.WasteBatch.quantity_kg)).scalar() or 0.0
    avg_recyclability = db.query(func.avg(models.WasteBatch.recyclability_score)).scalar() or 0.0
    
    material_dist = db.query(
        models.WasteBatch.fabric_type, func.sum(models.WasteBatch.quantity_kg)
    ).group_by(models.WasteBatch.fabric_type).all()
    material_distribution = {m[0]: m[1] for m in material_dist}
    
    cat_dist = db.query(
        models.WasteBatch.waste_category, func.count(models.WasteBatch.id)
    ).group_by(models.WasteBatch.waste_category).all()
    category_distribution = {c[0]: c[1] for c in cat_dist}
    
    cond_dist = db.query(
        models.WasteBatch.condition, func.count(models.WasteBatch.id)
    ).group_by(models.WasteBatch.condition).all()
    condition_distribution = {c[0]: c[1] for c in cond_dist}
    
    return schemas.AnalyticsResponse(
        total_batches=total_batches,
        total_weight=total_weight,
        material_distribution=material_distribution,
        category_distribution=category_distribution,
        condition_distribution=condition_distribution,
        avg_recyclability=avg_recyclability
    )

@router.get("/material-distribution")
def get_material_distribution(db: Session = Depends(get_db)):
    dist = db.query(
        models.WasteBatch.fabric_type, func.sum(models.WasteBatch.quantity_kg)
    ).group_by(models.WasteBatch.fabric_type).all()
    return {d[0]: d[1] for d in dist if d[0]}

@router.get("/category-distribution")
def get_category_distribution(db: Session = Depends(get_db)):
    dist = db.query(
        models.WasteBatch.waste_category, func.count(models.WasteBatch.id)
    ).group_by(models.WasteBatch.waste_category).all()
    return {d[0]: d[1] for d in dist if d[0]}

@router.get("/condition-distribution")
def get_condition_distribution(db: Session = Depends(get_db)):
    dist = db.query(
        models.WasteBatch.condition, func.count(models.WasteBatch.id)
    ).group_by(models.WasteBatch.condition).all()
    return {d[0]: d[1] for d in dist if d[0]}

@router.get("/environmental-impact")
def get_environmental_impact(db: Session = Depends(get_db)):
    total_weight = db.query(func.sum(models.WasteBatch.quantity_kg)).scalar() or 0.0
    # Dummy calculation for environmental impact
    return {
        "carbon_saved_kg": total_weight * 2.5,
        "water_saved_liters": total_weight * 100,
        "landfill_diverted_kg": total_weight
    }

@router.get("/recyclability-scores")
def get_recyclability_scores(db: Session = Depends(get_db)):
    scores = db.query(
        models.WasteBatch.fabric_type, func.avg(models.WasteBatch.recyclability_score)
    ).group_by(models.WasteBatch.fabric_type).all()
    return {s[0]: s[1] for s in scores if s[0]}
