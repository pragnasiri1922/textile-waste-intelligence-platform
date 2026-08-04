# Milestone 2: Material Recognition & Waste Classification

## Textile Waste Intelligence Platform — Technical Documentation

**Version:** 2.0.0  
**Date:** August 2026  
**Milestone Period:** Week 3 & 4

---

## 1. Overview

Milestone 2 implements the core intelligent processing capabilities of the platform:
- **Material Classification Engine** — Rule-based textile material recognition
- **Waste Categorization System** — Multi-factor decision engine for waste classification  
- **Recyclability Assessment** — Weighted scoring system with environmental impact metrics
- **Report Generation** — Structured batch and summary reporting

---

## 2. Architecture

### System Flow
```
User Input (Batch/Image) 
    --> Material Classification Engine (classify_material)
    --> Waste Categorizer (categorize_waste)
    --> Recyclability Assessor (assess_recyclability)
    --> Report Generator (generate_batch_report / generate_summary_report)
    --> Dashboard Display (Classification + Reports sections)
```

### Backend Structure
```
backend/app/
  services/
    __init__.py
    classification_engine.py    # Material detection & fiber analysis
    waste_categorizer.py        # Waste category decision engine
    recyclability_engine.py     # Recyclability scoring system
    report_generator.py         # Report generation engine
  routers/
    classification_router.py    # 6 new API endpoints
  models.py                     # Updated with TextileAnalysis model
  schemas.py                    # Classification schemas
```

### Frontend Structure
```
frontend/
  js/
    dashboard.js    # Updated: Classification + Reports sections
  css/
    styles.css      # Updated: 300+ new lines for M2 components
```

---

## 3. Backend Services

### 3.1 Classification Engine (`classification_engine.py`)

**Purpose:** Analyzes fabric properties to determine material composition.

**Features:**
- 10 material signature profiles (Cotton, Polyester, Wool, Silk, Denim, Nylon, Linen, Rayon, Acrylic, Mixed Fabrics)
- Each profile contains texture patterns, weight ranges, recyclability baselines, and market demand indices
- Secondary material trace detection
- Fiber composition percentage generation
- Image analysis simulation (placeholder for future ML model)

**Key Functions:**
| Function | Description |
|----------|-------------|
| `classify_material(fabric_type, color, condition)` | Main classification - returns material, confidence, fiber composition |
| `simulate_image_analysis(filename)` | Simulates CV-based textile recognition from uploaded images |

**Output Example:**
```json
{
  "material_detected": "Cotton",
  "confidence": 0.943,
  "fiber_composition": {"Cotton": 92.5, "Elastane": 7.5},
  "texture": "soft",
  "pattern": "twill",
  "properties": {
    "weight_class": "Medium Weight",
    "recyclability_base": 0.85,
    "market_demand_index": 0.9
  }
}
```

### 3.2 Waste Categorizer (`waste_categorizer.py`)

**Purpose:** Multi-factor decision system for assigning waste categories.

**Categories:**
| Category | Description | Priority |
|----------|-------------|----------|
| Reusable | Can be reused as-is | 1 |
| Repairable | Needs minor repairs | 2 |
| Recyclable | Suitable for fiber recycling | 3 |
| Upcyclable | Transform to higher-value | 2 |
| Compostable | Natural fibers for composting | 4 |
| Hazardous | Requires special handling | 6 |

**Scoring Factors:**
- Condition match (+30 points)
- Damage level assessment (+/-20 points)
- Contamination level check (+/-25 points)
- Recyclability threshold (+/-20 points)
- Special rules (compostable = natural fiber only, hazardous = high contamination)

### 3.3 Recyclability Engine (`recyclability_engine.py`)

**Purpose:** Weighted multi-factor scoring for recyclability assessment.

**Factor Weights:**
| Factor | Weight |
|--------|--------|
| Material Purity | 25% |
| Condition Quality | 20% |
| Contamination Impact | 20% |
| Damage Impact | 15% |
| Market Demand | 10% |
| Processing Feasibility | 10% |

**Grade Scale:**
| Grade | Score Range | Label |
|-------|------------|-------|
| A | 85-100 | Excellent - Highly Recyclable |
| B | 70-84 | Good - Readily Recyclable |
| C | 55-69 | Moderate - Recyclable with Processing |
| D | 40-54 | Low - Limited Recyclability |
| F | 0-39 | Poor - Difficult to Recycle |

**Environmental Impact Calculations:**
- Carbon saved: recyclable_kg * material_carbon_factor (kg CO2)
- Water saved: recyclable_kg * material_water_factor (liters)
- Energy saved: recyclable_kg * 15.5 (kWh)

### 3.4 Report Generator (`report_generator.py`)

**Purpose:** Generates structured classification reports.

**Report Types:**
1. **Batch Report** — Individual batch analysis with classification, categorization, recyclability, and environmental impact
2. **Summary Report** — Aggregate facility-level report across all batches with material distribution, grade distribution, and facility recommendations

---

## 4. API Endpoints

### Classification Router (`/api/classify`)

| Method | Endpoint | Description | Auth |
|--------|----------|-------------|------|
| POST | `/api/classify/analyze?batch_id={id}` | Run full classification pipeline on a batch | Required |
| POST | `/api/classify/image` | Upload textile image for analysis | Required |
| GET | `/api/classify/batch/{batch_id}` | Get existing analysis results | Required |
| POST | `/api/classify/bulk` | Bulk classify all unanalyzed batches | Required |
| GET | `/api/classify/report/{batch_id}` | Generate batch classification report | Required |
| GET | `/api/classify/summary-report` | Generate aggregate summary report | Required |

---

## 5. Database Schema Update

### TextileAnalysis Table (New)
| Column | Type | Description |
|--------|------|-------------|
| id | Integer (PK) | Auto-increment ID |
| batch_id | Integer (FK) | Reference to WasteBatch |
| material_detected | String | Classified material type |
| confidence | Float | Classification confidence (0-1) |
| texture | String | Detected texture |
| pattern | String | Detected pattern |
| fabric_color | String | Detected color |
| damage_level | String | Damage assessment |
| contamination_level | String | Contamination assessment |
| reuse_potential | String | Reuse potential description |
| disposal_recommendation | String | Recommended disposal method |
| recyclability_grade | String | Grade (A-F) |
| recyclability_score_computed | Float | Computed score (0-100) |
| analyzed_at | DateTime | Analysis timestamp |

---

## 6. Frontend Updates

### New Dashboard Sections

#### 6.1 Classification Page
- **Quick Classify Panel** — Select a batch and run instant analysis
- **Bulk Classify** — Analyze all unanalyzed batches in one click
- **Image Upload** — Drag-and-drop textile image analysis
- **Classification Results** — 6 detailed result cards:
  - Material Analysis (with confidence bar)
  - Fiber Composition (horizontal bar chart)
  - Waste Categorization (with reasoning)
  - Recyclability Assessment (circular score + grade badge)
  - Environmental Impact (4 metric displays)
  - Recommendations (actionable items)

#### 6.2 Reports Page
- **Summary Metrics** — Total analyzed, average grade, carbon/water saved
- **Generate Report** — One-click summary report generation
- **Report Display** — 6 structured report sections:
  - Overview (metrics summary)
  - Material Analysis (table)
  - Category Breakdown (horizontal bars)
  - Grade Distribution (badge display)
  - Environmental Impact (totals)
  - Facility Recommendations

### New CSS Components (300+ lines)
- Confidence progress bars with gradient fill
- Grade badges (A-F) with unique gradient colors
- Fiber composition horizontal bars
- Classification card grid with hover effects
- Circular SVG score indicator
- Recommendation items with checkmark prefix
- Environmental impact metric cards
- Report sections with glassmorphism
- Category breakdown bars
- Analyze/Bulk action buttons with gradient hover effects

---

## 7. Outcomes

| Requirement | Status |
|-------------|--------|
| Material classification engine operational | COMPLETE |
| Waste categorization workflows functional | COMPLETE |
| Recyclability assessment completed | COMPLETE |
| Waste classification reports generated | COMPLETE |
| 6 new API endpoints | COMPLETE |
| Frontend Classification dashboard | COMPLETE |
| Frontend Reports dashboard | COMPLETE |
| Environmental impact metrics | COMPLETE |

---

## 8. Running the Platform

### Start the Server
```bash
cd textile-waste-intelligence-platform
python run.py
```

### Access Points
| URL | Description |
|-----|-------------|
| http://127.0.0.1:8000/app | Frontend Dashboard |
| http://127.0.0.1:8000/docs | API Documentation (Swagger) |
| http://127.0.0.1:8000/ | API Root |

### Default Login
- **Username:** admin
- **Password:** admin123

---

## 9. Technology Stack

| Component | Technology |
|-----------|-----------|
| Backend | Python 3.x, FastAPI, SQLAlchemy, Pydantic |
| Database | SQLite |
| Frontend | HTML5, CSS3, Vanilla JavaScript |
| Charts | Chart.js |
| Auth | JWT (python-jose), bcrypt (passlib) |
| Server | Uvicorn (ASGI) |
