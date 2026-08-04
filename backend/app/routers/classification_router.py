from fastapi import APIRouter, Depends, HTTPException, UploadFile, File
from sqlalchemy.orm import Session
from datetime import datetime, timezone

import models, auth
from database import get_db
from services.classification_engine import classify_material, simulate_image_analysis
from services.waste_categorizer import categorize_waste, get_disposal_recommendation
from services.recyclability_engine import assess_recyclability
from services.report_generator import generate_batch_report, generate_summary_report

router = APIRouter(prefix="/api/classify", tags=["Classification & Analysis"])


@router.post("/analyze")
def analyze_batch(
    batch_id: int,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(auth.get_current_user),
):
    batch = db.query(models.WasteBatch).filter(models.WasteBatch.id == batch_id).first()
    if not batch:
        raise HTTPException(status_code=404, detail="Batch not found")

    classification = classify_material(batch.fabric_type, batch.color or '', batch.condition or '')
    categorization = categorize_waste(
        batch.fabric_type, batch.condition or 'Fair',
        batch.damage_level or 'None', batch.contamination_level or 'None',
        batch.recyclability_score or 0.5,
    )
    disposal_rec = get_disposal_recommendation(categorization['recommended_category'], batch.fabric_type)
    categorization['disposal_recommendation'] = disposal_rec

    recyclability = assess_recyclability(
        batch.fabric_type, batch.condition or 'Fair',
        batch.damage_level or 'None', batch.contamination_level or 'None',
        batch.quantity_kg or 0,
    )

    analysis = models.TextileAnalysis(
        batch_id=batch.id,
        material_detected=classification['material_detected'],
        confidence=classification['confidence'],
        texture=classification.get('texture', ''),
        pattern=classification.get('pattern', ''),
        fabric_color=batch.color or '',
        damage_level=batch.damage_level or 'None',
        contamination_level=batch.contamination_level or 'None',
        reuse_potential=recyclability.get('reuse_potential', ''),
        disposal_recommendation=disposal_rec,
        recyclability_grade=recyclability.get('grade', 'C'),
        recyclability_score_computed=recyclability.get('recyclability_score', 0),
        analyzed_at=datetime.now(timezone.utc),
    )
    db.add(analysis)
    db.commit()
    db.refresh(analysis)

    return {
        'batch_id': batch.batch_id,
        'analysis_id': analysis.id,
        'classification': classification,
        'categorization': categorization,
        'recyclability': recyclability,
    }


@router.post("/image")
async def analyze_image(
    file: UploadFile = File(...),
    current_user: models.User = Depends(auth.get_current_user),
):
    if not file.content_type or not file.content_type.startswith('image/'):
        raise HTTPException(status_code=400, detail="File must be an image")
    result = simulate_image_analysis(file.filename or 'uploaded_image')
    return result


@router.get("/batch/{batch_id}")
def get_batch_analysis(
    batch_id: int,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(auth.get_current_user),
):
    batch = db.query(models.WasteBatch).filter(models.WasteBatch.id == batch_id).first()
    if not batch:
        raise HTTPException(status_code=404, detail="Batch not found")

    analyses = (
        db.query(models.TextileAnalysis)
        .filter(models.TextileAnalysis.batch_id == batch.id)
        .order_by(models.TextileAnalysis.analyzed_at.desc())
        .all()
    )
    return {
        'batch_id': batch.batch_id,
        'fabric_type': batch.fabric_type,
        'analyses': [
            {
                'id': a.id, 'material_detected': a.material_detected,
                'confidence': a.confidence, 'texture': a.texture,
                'pattern': a.pattern, 'recyclability_grade': a.recyclability_grade,
                'recyclability_score': a.recyclability_score_computed,
                'reuse_potential': a.reuse_potential,
                'disposal_recommendation': a.disposal_recommendation,
                'analyzed_at': a.analyzed_at.isoformat() if a.analyzed_at else None,
            }
            for a in analyses
        ],
    }


@router.post("/bulk")
def bulk_classify(
    db: Session = Depends(get_db),
    current_user: models.User = Depends(auth.get_current_user),
):
    analyzed_ids = db.query(models.TextileAnalysis.batch_id).distinct().subquery()
    unanalyzed = db.query(models.WasteBatch).filter(~models.WasteBatch.id.in_(analyzed_ids)).all()

    results = []
    for batch in unanalyzed:
        classification = classify_material(batch.fabric_type, batch.color or '', batch.condition or '')
        categorization = categorize_waste(
            batch.fabric_type, batch.condition or 'Fair',
            batch.damage_level or 'None', batch.contamination_level or 'None',
            batch.recyclability_score or 0.5,
        )
        recyclability = assess_recyclability(
            batch.fabric_type, batch.condition or 'Fair',
            batch.damage_level or 'None', batch.contamination_level or 'None',
            batch.quantity_kg or 0,
        )
        disposal_rec = get_disposal_recommendation(categorization['recommended_category'], batch.fabric_type)

        analysis = models.TextileAnalysis(
            batch_id=batch.id,
            material_detected=classification['material_detected'],
            confidence=classification['confidence'],
            texture=classification.get('texture', ''),
            pattern=classification.get('pattern', ''),
            fabric_color=batch.color or '',
            damage_level=batch.damage_level or 'None',
            contamination_level=batch.contamination_level or 'None',
            reuse_potential=recyclability.get('reuse_potential', ''),
            disposal_recommendation=disposal_rec,
            recyclability_grade=recyclability.get('grade', 'C'),
            recyclability_score_computed=recyclability.get('recyclability_score', 0),
            analyzed_at=datetime.now(timezone.utc),
        )
        db.add(analysis)
        results.append({
            'batch_id': batch.batch_id, 'material': classification['material_detected'],
            'category': categorization['recommended_category'],
            'grade': recyclability['grade'], 'score': recyclability['recyclability_score'],
        })

    db.commit()
    return {'total_analyzed': len(results), 'results': results}


@router.get("/report/{batch_id}")
def get_batch_report(
    batch_id: int,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(auth.get_current_user),
):
    batch = db.query(models.WasteBatch).filter(models.WasteBatch.id == batch_id).first()
    if not batch:
        raise HTTPException(status_code=404, detail="Batch not found")

    batch_data = {
        'batch_id': batch.batch_id, 'fabric_type': batch.fabric_type,
        'source': batch.source, 'quantity_kg': batch.quantity_kg,
        'color': batch.color, 'condition': batch.condition,
    }
    classification = classify_material(batch.fabric_type, batch.color or '', batch.condition or '')
    categorization = categorize_waste(
        batch.fabric_type, batch.condition or 'Fair',
        batch.damage_level or 'None', batch.contamination_level or 'None',
        batch.recyclability_score or 0.5,
    )
    categorization['disposal_recommendation'] = get_disposal_recommendation(
        categorization['recommended_category'], batch.fabric_type
    )
    recyclability = assess_recyclability(
        batch.fabric_type, batch.condition or 'Fair',
        batch.damage_level or 'None', batch.contamination_level or 'None',
        batch.quantity_kg or 0,
    )
    return generate_batch_report(batch_data, classification, categorization, recyclability)


@router.get("/summary-report")
def get_summary_report(
    db: Session = Depends(get_db),
    current_user: models.User = Depends(auth.get_current_user),
):
    batches = db.query(models.WasteBatch).all()
    batches_data = [
        {
            'batch_id': b.batch_id, 'fabric_type': b.fabric_type,
            'source': b.source, 'quantity_kg': b.quantity_kg,
            'waste_category': b.waste_category, 'recyclability_score': b.recyclability_score,
        }
        for b in batches
    ]
    return generate_summary_report(batches_data)
