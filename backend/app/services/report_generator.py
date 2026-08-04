"""
Waste Classification Report Generator
"""
from datetime import datetime, timezone
from typing import Dict, List


def generate_batch_report(batch_data: Dict, classification: Dict, categorization: Dict, recyclability: Dict) -> Dict:
    return {
        'report_type': 'Batch Classification Report',
        'generated_at': datetime.now(timezone.utc).isoformat(),
        'platform_version': '2.0.0',
        'batch_info': {
            'batch_id': batch_data.get('batch_id', 'N/A'),
            'fabric_type': batch_data.get('fabric_type', 'Unknown'),
            'source': batch_data.get('source', 'Unknown'),
            'quantity_kg': batch_data.get('quantity_kg', 0),
            'color': batch_data.get('color', 'Unknown'),
            'condition': batch_data.get('condition', 'Unknown'),
        },
        'material_classification': {
            'detected_material': classification.get('material_detected', 'Unknown'),
            'confidence': classification.get('confidence', 0),
            'fiber_composition': classification.get('fiber_composition', {}),
            'texture': classification.get('texture', 'Unknown'),
            'pattern': classification.get('pattern', 'Unknown'),
        },
        'waste_categorization': {
            'category': categorization.get('recommended_category', 'Unknown'),
            'confidence': categorization.get('confidence', 0),
            'description': categorization.get('category_description', ''),
            'processing_cost': categorization.get('processing_cost', 'Unknown'),
            'environmental_benefit': categorization.get('environmental_benefit', 'Unknown'),
            'reasoning': categorization.get('reasoning', []),
        },
        'recyclability_assessment': {
            'score': recyclability.get('recyclability_score', 0),
            'grade': recyclability.get('grade', 'F'),
            'grade_label': recyclability.get('grade_label', 'Unknown'),
            'reuse_potential': recyclability.get('reuse_potential', 'Unknown'),
            'recommendations': recyclability.get('recommendations', []),
            'environmental_impact': recyclability.get('environmental_impact', {}),
        },
        'disposal_recommendation': categorization.get('disposal_recommendation', 'Standard processing'),
    }


def generate_summary_report(batches_data: List[Dict]) -> Dict:
    if not batches_data:
        return {'report_type': 'Summary Report', 'error': 'No data available'}

    total_batches = len(batches_data)
    total_weight = sum(b.get('quantity_kg', 0) for b in batches_data)
    material_counts, material_weights, category_counts = {}, {}, {}
    grade_counts = {'A': 0, 'B': 0, 'C': 0, 'D': 0, 'F': 0}
    total_recyclability = 0

    for b in batches_data:
        mat = b.get('fabric_type', 'Unknown')
        material_counts[mat] = material_counts.get(mat, 0) + 1
        material_weights[mat] = material_weights.get(mat, 0) + b.get('quantity_kg', 0)
        cat = b.get('waste_category', 'Unknown')
        category_counts[cat] = category_counts.get(cat, 0) + 1
        score = b.get('recyclability_score', 0)
        total_recyclability += score
        g = _score_to_grade(score * 100 if score <= 1 else score)
        grade_counts[g] = grade_counts.get(g, 0) + 1

    avg = total_recyclability / total_batches if total_batches > 0 else 0

    return {
        'report_type': 'Waste Classification Summary Report',
        'generated_at': datetime.now(timezone.utc).isoformat(),
        'overview': {
            'total_batches_analyzed': total_batches,
            'total_weight_kg': round(total_weight, 1),
            'average_recyclability': round(avg, 3),
            'overall_grade': _score_to_grade(avg * 100 if avg <= 1 else avg),
        },
        'material_analysis': {
            'distribution_by_count': material_counts,
            'distribution_by_weight_kg': {k: round(v, 1) for k, v in material_weights.items()},
        },
        'category_breakdown': category_counts,
        'grade_distribution': grade_counts,
        'environmental_impact': {
            'total_carbon_saved_kg': round(total_weight * 2.5 * avg, 1),
            'total_water_saved_liters': round(total_weight * 80 * avg, 1),
            'total_landfill_diverted_kg': round(total_weight * avg, 1),
        },
        'recommendations': _gen_summary_recs(material_counts, category_counts, avg),
    }


def _score_to_grade(score: float) -> str:
    if score >= 85: return 'A'
    elif score >= 70: return 'B'
    elif score >= 55: return 'C'
    elif score >= 40: return 'D'
    else: return 'F'


def _gen_summary_recs(materials: Dict, categories: Dict, avg: float) -> List[str]:
    recs = []
    if avg >= 0.7:
        recs.append('Facility performing well with high average recyclability.')
    elif avg >= 0.5:
        recs.append('Moderate recyclability. Consider better pre-sorting equipment.')
    else:
        recs.append('Low recyclability. Review incoming waste streams.')

    dominant = max(materials, key=materials.get) if materials else None
    if dominant:
        recs.append(f'Primary material stream: {dominant}. Consider dedicated processing line.')

    hazardous = categories.get('Hazardous Textile Waste', 0)
    if hazardous > 0:
        recs.append(f'ALERT: {hazardous} hazardous waste batches detected.')
    recs.append('Schedule quarterly waste audits to track recyclability trends.')
    return recs
