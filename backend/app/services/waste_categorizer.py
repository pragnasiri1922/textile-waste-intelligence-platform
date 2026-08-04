"""
Waste Categorization Engine
Multi-factor decision system for categorizing textile waste.
"""
from typing import Dict, List

WASTE_CATEGORIES = {
    'Reusable': {
        'description': 'Textiles that can be reused as-is with minimal processing',
        'conditions': ['Good', 'Reusable'],
        'max_damage': 'None', 'max_contamination': 'None',
        'min_quality': 0.7, 'processing_cost': 'Low', 'environmental_benefit': 'Very High',
    },
    'Repairable': {
        'description': 'Textiles needing minor repairs before reuse',
        'conditions': ['Fair', 'Damaged'],
        'max_damage': 'Minor', 'max_contamination': 'Low',
        'min_quality': 0.5, 'processing_cost': 'Medium', 'environmental_benefit': 'High',
    },
    'Recyclable': {
        'description': 'Textiles suitable for fiber-to-fiber recycling',
        'conditions': ['Recyclable', 'Fair', 'Good'],
        'max_damage': 'Moderate', 'max_contamination': 'Low',
        'min_quality': 0.3, 'processing_cost': 'Medium', 'environmental_benefit': 'High',
    },
    'Upcyclable': {
        'description': 'Textiles that can be transformed into higher-value products',
        'conditions': ['Good', 'Fair', 'Recyclable'],
        'max_damage': 'Minor', 'max_contamination': 'None',
        'min_quality': 0.6, 'processing_cost': 'Medium-High', 'environmental_benefit': 'Very High',
    },
    'Compostable': {
        'description': 'Natural fiber textiles suitable for composting',
        'conditions': ['Damaged', 'Contaminated', 'Fair'],
        'max_damage': 'Severe', 'max_contamination': 'Moderate',
        'min_quality': 0.0, 'processing_cost': 'Low', 'environmental_benefit': 'Medium',
    },
    'Hazardous Textile Waste': {
        'description': 'Contaminated textiles requiring special handling',
        'conditions': ['Contaminated'],
        'max_damage': 'Severe', 'max_contamination': 'High',
        'min_quality': 0.0, 'processing_cost': 'Very High', 'environmental_benefit': 'Low',
    },
}

DAMAGE_LEVELS = {'None': 0, 'Minor': 1, 'Moderate': 2, 'Severe': 3}
CONTAMINATION_LEVELS = {'None': 0, 'Low': 1, 'Moderate': 2, 'High': 3}
NATURAL_FIBERS = ['Cotton', 'Linen', 'Wool', 'Silk', 'Hemp', 'Jute']


def categorize_waste(
    fabric_type: str, condition: str, damage_level: str = 'None',
    contamination_level: str = 'None', recyclability_score: float = 0.5,
) -> Dict:
    scores = {}
    reasons = {}
    damage_val = DAMAGE_LEVELS.get(damage_level, 1)
    contam_val = CONTAMINATION_LEVELS.get(contamination_level, 1)

    for cat_name, cat_info in WASTE_CATEGORIES.items():
        score = 0.0
        cat_reasons = []

        if condition in cat_info['conditions']:
            score += 30
            cat_reasons.append(f'Condition "{condition}" matches category')

        max_dmg = DAMAGE_LEVELS.get(cat_info['max_damage'], 3)
        if damage_val <= max_dmg:
            score += 20
            cat_reasons.append(f'Damage level acceptable ({damage_level})')
        else:
            score -= 20

        max_contam = CONTAMINATION_LEVELS.get(cat_info['max_contamination'], 3)
        if contam_val <= max_contam:
            score += 20
            cat_reasons.append(f'Contamination level acceptable ({contamination_level})')
        else:
            score -= 25

        if recyclability_score >= cat_info['min_quality']:
            score += 20
            cat_reasons.append(f'Recyclability score ({recyclability_score:.1%}) meets minimum')

        if cat_name == 'Compostable':
            is_natural = any(nf.lower() in fabric_type.lower() for nf in NATURAL_FIBERS)
            if is_natural:
                score += 10
                cat_reasons.append('Natural fiber detected - compostable')
            else:
                score -= 40

        if cat_name == 'Hazardous Textile Waste' and contam_val >= 2:
            score += 30
            cat_reasons.append('High contamination requires hazardous handling')

        scores[cat_name] = max(score, 0)
        reasons[cat_name] = cat_reasons

    best_category = max(scores, key=scores.get)
    ranked = sorted(scores.items(), key=lambda x: x[1], reverse=True)

    return {
        'recommended_category': best_category,
        'confidence': round(scores[best_category] / 100, 3),
        'category_description': WASTE_CATEGORIES[best_category]['description'],
        'processing_cost': WASTE_CATEGORIES[best_category]['processing_cost'],
        'environmental_benefit': WASTE_CATEGORIES[best_category]['environmental_benefit'],
        'reasoning': reasons[best_category],
        'all_scores': {k: round(v / 100, 3) for k, v in ranked},
        'alternative_categories': [
            {'category': cat, 'score': round(sc / 100, 3), 'reasoning': reasons[cat]}
            for cat, sc in ranked[1:3]
        ],
    }


def get_disposal_recommendation(category: str, fabric_type: str) -> str:
    recommendations = {
        'Reusable': f'Direct resale or donation. {fabric_type} items in good condition have strong secondary market demand.',
        'Repairable': f'Route to repair workshop. Minor {fabric_type} repairs can restore item to reusable condition.',
        'Recyclable': f'Send to fiber recycling facility. {fabric_type} can be broken down and respun into new yarns.',
        'Upcyclable': f'Forward to upcycling partners. {fabric_type} has good potential for value-added transformation.',
        'Compostable': f'Route to industrial composting. Natural {fabric_type} fibers will biodegrade in 3-6 months.',
        'Hazardous Textile Waste': f'Hazardous waste protocol required. {fabric_type} items must be decontaminated.',
    }
    return recommendations.get(category, f'Standard processing for {fabric_type}.')
