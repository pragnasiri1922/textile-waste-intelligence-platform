"""
Recyclability Assessment Engine
Weighted multi-factor scoring system for textile recyclability.
"""
from typing import Dict, List

FACTOR_WEIGHTS = {
    'material_purity': 0.25, 'condition_quality': 0.20,
    'contamination_impact': 0.20, 'damage_impact': 0.15,
    'market_demand': 0.10, 'processing_feasibility': 0.10,
}

MATERIAL_RECYCLABILITY = {
    'Cotton': {'purity': 0.90, 'process_ease': 0.85, 'demand': 0.92},
    'Polyester': {'purity': 0.75, 'process_ease': 0.70, 'demand': 0.88},
    'Wool': {'purity': 0.80, 'process_ease': 0.75, 'demand': 0.82},
    'Silk': {'purity': 0.65, 'process_ease': 0.55, 'demand': 0.70},
    'Denim': {'purity': 0.88, 'process_ease': 0.80, 'demand': 0.95},
    'Nylon': {'purity': 0.70, 'process_ease': 0.65, 'demand': 0.78},
    'Linen': {'purity': 0.85, 'process_ease': 0.80, 'demand': 0.75},
    'Rayon': {'purity': 0.60, 'process_ease': 0.55, 'demand': 0.62},
    'Acrylic': {'purity': 0.50, 'process_ease': 0.45, 'demand': 0.55},
    'Mixed Fabrics': {'purity': 0.35, 'process_ease': 0.30, 'demand': 0.45},
}

CONDITION_SCORES = {
    'Good': 1.0, 'Reusable': 0.9, 'Fair': 0.7, 'Recyclable': 0.8,
    'Damaged': 0.4, 'Contaminated': 0.2,
}
DAMAGE_SCORES = {'None': 1.0, 'Minor': 0.8, 'Moderate': 0.5, 'Severe': 0.2}
CONTAMINATION_SCORES = {'None': 1.0, 'Low': 0.75, 'Moderate': 0.4, 'High': 0.1}


def assess_recyclability(
    fabric_type: str, condition: str, damage_level: str = 'None',
    contamination_level: str = 'None', quantity_kg: float = 0,
) -> Dict:
    mat_key = _match_material_key(fabric_type)
    mat_props = MATERIAL_RECYCLABILITY.get(mat_key, MATERIAL_RECYCLABILITY['Mixed Fabrics'])

    factors = {
        'material_purity': mat_props['purity'],
        'condition_quality': CONDITION_SCORES.get(condition, 0.5),
        'contamination_impact': CONTAMINATION_SCORES.get(contamination_level, 0.5),
        'damage_impact': DAMAGE_SCORES.get(damage_level, 0.5),
        'market_demand': mat_props['demand'],
        'processing_feasibility': mat_props['process_ease'],
    }

    weighted_score = sum(factors[f] * FACTOR_WEIGHTS[f] for f in FACTOR_WEIGHTS)
    final_score = round(weighted_score * 100, 1)
    grade = _score_to_grade(final_score)

    env_impact = _calc_env_impact(final_score, quantity_kg, mat_key)
    recommendations = _gen_recommendations(grade, factors, mat_key)

    return {
        'recyclability_score': final_score,
        'grade': grade,
        'grade_label': _grade_label(grade),
        'factor_breakdown': {
            k: {'score': round(v * 100, 1), 'weight': FACTOR_WEIGHTS[k],
                 'weighted_contribution': round(v * FACTOR_WEIGHTS[k] * 100, 1)}
            for k, v in factors.items()
        },
        'environmental_impact': env_impact,
        'recommendations': recommendations,
        'reuse_potential': _assess_reuse(factors),
    }


def _match_material_key(fabric_type: str) -> str:
    ft = fabric_type.lower().strip()
    for key in MATERIAL_RECYCLABILITY:
        if key.lower() in ft or ft in key.lower():
            return key
    return 'Mixed Fabrics'


def _score_to_grade(score: float) -> str:
    if score >= 85: return 'A'
    elif score >= 70: return 'B'
    elif score >= 55: return 'C'
    elif score >= 40: return 'D'
    else: return 'F'


def _grade_label(grade: str) -> str:
    return {'A': 'Excellent - Highly Recyclable', 'B': 'Good - Readily Recyclable',
            'C': 'Moderate - Recyclable with Processing', 'D': 'Low - Limited Recyclability',
            'F': 'Poor - Difficult to Recycle'}.get(grade, 'Unknown')


def _calc_env_impact(score: float, quantity_kg: float, material: str) -> Dict:
    rate = score / 100
    recyclable_kg = quantity_kg * rate
    carbon = {'Cotton': 2.1, 'Polyester': 3.8, 'Denim': 2.5}.get(material, 2.5)
    water = {'Cotton': 120, 'Polyester': 60, 'Denim': 100}.get(material, 80)
    return {
        'recyclable_weight_kg': round(recyclable_kg, 1),
        'carbon_saved_kg': round(recyclable_kg * carbon, 1),
        'water_saved_liters': round(recyclable_kg * water, 1),
        'landfill_diverted_kg': round(recyclable_kg, 1),
        'energy_saved_kwh': round(recyclable_kg * 15.5, 1),
    }


def _assess_reuse(factors: Dict) -> str:
    c, d = factors['condition_quality'], factors['damage_impact']
    if c >= 0.8 and d >= 0.8: return 'High - Suitable for direct resale or donation'
    elif c >= 0.6 and d >= 0.5: return 'Medium - Suitable after minor repairs'
    elif c >= 0.3: return 'Low - Fiber recycling recommended'
    else: return 'Very Low - Industrial processing or disposal'


def _gen_recommendations(grade: str, factors: Dict, material: str) -> List[str]:
    recs = []
    if grade in ('A', 'B'):
        recs.append(f'Prioritize for fiber-to-fiber recycling - {material} has high recovery potential')
        recs.append('Consider upcycling partnerships for premium waste streams')
    elif grade == 'C':
        recs.append(f'Standard recycling processing recommended for {material}')
        recs.append('Pre-sort by color to maximize recycled fiber quality')
    elif grade == 'D':
        recs.append('Consider downcycling to insulation or industrial rags')
    else:
        recs.append('Evaluate for energy recovery (waste-to-energy)')

    if factors['contamination_impact'] < 0.5:
        recs.append('PRIORITY: Decontamination required before processing')
    if factors['damage_impact'] < 0.5:
        recs.append('Note: Significant damage may reduce fiber recovery yield')
    return recs
