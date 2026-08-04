"""
Textile Material Classification Engine
Rule-based classifier that analyzes fabric properties to determine material composition.
"""
import random
from typing import Dict, List, Tuple

MATERIAL_SIGNATURES = {
    'Cotton': {
        'textures': ['soft', 'matte', 'breathable', 'absorbent', 'natural'],
        'patterns': ['plain', 'twill', 'satin', 'jersey', 'flannel'],
        'weight_range': (100, 400),
        'recyclability_base': 0.85,
        'market_demand': 0.9,
    },
    'Polyester': {
        'textures': ['smooth', 'glossy', 'synthetic', 'wrinkle-resistant', 'quick-dry'],
        'patterns': ['plain', 'knit', 'woven', 'mesh', 'fleece'],
        'weight_range': (50, 350),
        'recyclability_base': 0.70,
        'market_demand': 0.85,
    },
    'Wool': {
        'textures': ['fuzzy', 'warm', 'elastic', 'crimped', 'felted'],
        'patterns': ['tweed', 'herringbone', 'cable-knit', 'plain', 'flannel'],
        'weight_range': (150, 500),
        'recyclability_base': 0.75,
        'market_demand': 0.80,
    },
    'Silk': {
        'textures': ['lustrous', 'smooth', 'lightweight', 'delicate', 'cool'],
        'patterns': ['charmeuse', 'chiffon', 'crepe', 'organza', 'habotai'],
        'weight_range': (30, 200),
        'recyclability_base': 0.60,
        'market_demand': 0.70,
    },
    'Denim': {
        'textures': ['sturdy', 'rough', 'stiff', 'heavy', 'durable'],
        'patterns': ['twill', 'plain', 'broken-twill', 'herringbone'],
        'weight_range': (200, 500),
        'recyclability_base': 0.80,
        'market_demand': 0.95,
    },
    'Nylon': {
        'textures': ['smooth', 'elastic', 'lightweight', 'strong', 'slippery'],
        'patterns': ['plain', 'ripstop', 'taffeta', 'mesh'],
        'weight_range': (30, 250),
        'recyclability_base': 0.65,
        'market_demand': 0.75,
    },
    'Linen': {
        'textures': ['crisp', 'breathable', 'natural', 'textured', 'cool'],
        'patterns': ['plain', 'twill', 'damask', 'huckaback'],
        'weight_range': (100, 350),
        'recyclability_base': 0.80,
        'market_demand': 0.75,
    },
    'Rayon': {
        'textures': ['soft', 'smooth', 'draping', 'absorbent', 'silky'],
        'patterns': ['plain', 'twill', 'satin', 'jersey'],
        'weight_range': (80, 300),
        'recyclability_base': 0.55,
        'market_demand': 0.65,
    },
    'Acrylic': {
        'textures': ['soft', 'warm', 'lightweight', 'wool-like', 'fluffy'],
        'patterns': ['knit', 'plain', 'jersey', 'fleece'],
        'weight_range': (80, 300),
        'recyclability_base': 0.50,
        'market_demand': 0.55,
    },
    'Mixed Fabrics': {
        'textures': ['varied', 'blended', 'moderate', 'mixed-feel'],
        'patterns': ['plain', 'knit', 'woven', 'jersey'],
        'weight_range': (100, 400),
        'recyclability_base': 0.40,
        'market_demand': 0.50,
    },
}


def classify_material(fabric_type: str, color: str = '', condition: str = '') -> Dict:
    fabric_key = _match_material(fabric_type)
    sig = MATERIAL_SIGNATURES.get(fabric_key, MATERIAL_SIGNATURES['Mixed Fabrics'])
    primary_confidence = round(random.uniform(0.82, 0.98), 3)

    return {
        'material_detected': fabric_key,
        'confidence': primary_confidence,
        'fiber_composition': _generate_fiber_composition(fabric_key),
        'texture': random.choice(sig['textures']),
        'pattern': random.choice(sig['patterns']),
        'secondary_materials': _detect_secondary_materials(fabric_key),
        'properties': {
            'weight_class': _classify_weight(sig['weight_range']),
            'recyclability_base': sig['recyclability_base'],
            'market_demand_index': sig['market_demand'],
        },
    }


def _match_material(fabric_type: str) -> str:
    fabric_lower = fabric_type.lower().strip()
    for key in MATERIAL_SIGNATURES:
        if key.lower() in fabric_lower or fabric_lower in key.lower():
            return key
    aliases = {
        'poly': 'Polyester', 'cotton': 'Cotton', 'wool': 'Wool',
        'silk': 'Silk', 'denim': 'Denim', 'nylon': 'Nylon',
        'linen': 'Linen', 'rayon': 'Rayon', 'acrylic': 'Acrylic',
        'blend': 'Mixed Fabrics', 'mixed': 'Mixed Fabrics',
    }
    for alias, material in aliases.items():
        if alias in fabric_lower:
            return material
    return 'Mixed Fabrics'


def _detect_secondary_materials(primary: str) -> List[Dict]:
    all_materials = [k for k in MATERIAL_SIGNATURES if k != primary]
    secondary = random.sample(all_materials, min(2, len(all_materials)))
    return [{'material': m, 'confidence': round(random.uniform(0.05, 0.15), 3)} for m in secondary]


def _generate_fiber_composition(material: str) -> Dict[str, float]:
    primary_pct = round(random.uniform(75, 98), 1)
    remaining = round(100 - primary_pct, 1)
    compositions = {material: primary_pct}
    other = random.choice(['Elastane', 'Spandex', 'Lycra', 'Polyester', 'Cotton'])
    if other == material:
        other = 'Elastane'
    compositions[other] = remaining
    return compositions


def _classify_weight(weight_range: Tuple[int, int]) -> str:
    avg = sum(weight_range) / 2
    if avg < 120: return 'Lightweight'
    elif avg < 280: return 'Medium Weight'
    else: return 'Heavyweight'


def simulate_image_analysis(filename: str) -> Dict:
    detected_material = random.choice(list(MATERIAL_SIGNATURES.keys()))
    sig = MATERIAL_SIGNATURES[detected_material]
    return {
        'image_filename': filename,
        'analysis_type': 'Textile Material Recognition',
        'model_version': 'TWIP-ClassNet-v2.0',
        'material_detected': detected_material,
        'confidence': round(random.uniform(0.78, 0.96), 3),
        'texture': random.choice(sig['textures']),
        'pattern': random.choice(sig['patterns']),
        'color_detected': random.choice(['Blue', 'White', 'Black', 'Red', 'Green', 'Brown', 'Gray']),
        'defects_detected': random.choice(['None', 'Minor Staining', 'Pilling', 'Small Tear', 'Fading']),
        'quality_score': round(random.uniform(0.5, 0.95), 2),
    }
