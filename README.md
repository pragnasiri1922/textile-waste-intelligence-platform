# ♻️ Textile Waste Intelligence Platform

## Description
The Textile Waste Intelligence Platform is an innovative AI-powered solution designed to manage, categorize, and optimize the processing of textile waste. It provides tools for inventory tracking, material classification, and recyclability assessment to promote circular economy practices in the textile industry.

## Tech Stack
* **Backend:** FastAPI, Python, SQLAlchemy
* **Frontend:** HTML, CSS, JavaScript, Chart.js
* **Database:** SQLite
* **Data Processing:** Pandas

## Architecture Overview
The platform utilizes a 3-tier architecture:
1. **Frontend Presentation Layer:** Interactive dashboards and UI built with HTML/CSS/JS.
2. **Backend API Layer:** RESTful APIs built with FastAPI to handle business logic and model serving.
3. **Data Layer:** SQLite database for robust data storage and retrieval.

## Milestone-1 Features
* User Authentication & Role-Based Access Control
* Textile Inventory & Waste Management Dashboard
* Foundational Textile Image Analysis Engine
* Material Classification Engine
* Textile Waste Classification Engine
* Seed data and sample datasets included

## Setup Instructions
1. Clone the repository
2. Navigate to the project root: `cd textile-waste-intelligence-platform`
3. Install dependencies: `pip install -r requirements.txt`
4. Run the seed script: `python database/seed_data.py`
5. Start the server: `python run.py`
6. Access the API at http://127.0.0.1:8000 and the frontend by opening `frontend/index.html`.

## API Endpoints

| Endpoint | Method | Description |
|---|---|---|
| `/api/auth/token` | POST | Login and get JWT token |
| `/api/users/me` | GET | Get current user profile |
| `/api/waste/batches` | GET | List all waste batches |
| `/api/waste/batches` | POST | Register a new waste batch |
| `/api/analysis/predict` | POST | Mock endpoint for image analysis |

## Folder Structure
```
textile-waste-intelligence-platform/
├── backend/          # FastAPI application
├── database/         # SQLite DB, schema, and seed scripts
├── dataset/          # Sample CSV datasets
├── docs/             # Documentation
├── frontend/         # HTML/CSS/JS dashboard
├── requirements.txt  # Dependencies
└── run.py            # Startup script
```

## Screenshots
*(Add screenshots of the dashboard here)*

## License
MIT License
