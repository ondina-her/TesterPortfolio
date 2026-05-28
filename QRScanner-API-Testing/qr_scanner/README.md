# QR Code Scanner - Software Tester Portfolio

[![Python](https://img.shields.io/badge/python-3.12-blue.svg)]()
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)]()
[![Tests](https://img.shields.io/badge/tests-pytest-green.svg)]()

## 📋 Project Overview
This project demonstrates a **FastAPI** backend with a **QR code scanner** frontend.  
It includes **Selenium + pytest** automated tests aligned with JIRA Sprint tasks (STQC-5 to STQC-9).

## 🚀 Features
- FastAPI server with QR scanner page
- Camera-based QR code scanning
- SQLAlchemy database integration (SQLite for demo)
- Automated UI tests with Selenium + pytest

## Database Design
The backend uses **two tables**:
- **Item** → represents the decoded QR content (e.g., a link or text).
- **Scan** → represents the scanning event (time, source, and the QR text), linked directly to an Item.

👉 Each Scan points to its Item via `item_id`


## 🧪 Test Coverage

 Manual tests: Postman on `/items/`, `/scans/`. Automated tests: Selenium + pytest (STQC-5–STQC-9).

- STQC-5 Environment setup
- STQC-6 Valid QR test
- STQC-7 Invalid QR test
- STQC-8 Empty request test
- STQC-9 UI validation

## 📋 Project Scope and Objectives
See `TestCases.md` for the full scope, objectives, and detailed test cases.

## 🧪 Test Cases Documentation
A detailed test case document (STQC‑5 to STQC‑9) is included in this repository.  
It covers:
- Functional tests with Selenium (valid QR, invalid QR, empty QR, UI validation).
- API tests with Postman (Items and Scans endpoints).
- Negative cases (empty fields, invalid IDs).

👉 See `TestCases.md` for the full list of test cases, objectives, steps, and expected results.


## 📂 Project Structure
app/           # FastAPI backend
static/        # CSS, JS, images
templates/     # HTML templates
Test/          # Selenium + pytest tests, Postman

## 📦 Requirements
All dependencies are listed in `requirements.txt`.  
Install them with:
```bash
pip install -r requirements.txt
```

## ⚙️ Setup
1. Clone the repo:
   ```bash
   git clone https://github.com/yourusername/qr-scanner-portfolio.git

## Virtual Enviroment
python -m venv .venv
source .venv/bin/activate   # Linux/Mac
.venv\Scripts\activate      # Windows

## ▶️ Usage
#Run the app
uvicorn app.app:app --reload

#Run test
pytest Test/ -v
- Open http://localhost:8000 in your browser.

- Click Start Scanner and show a QR code to your camera.

- Decoded text will appear in the result box.

# Postman Tests
This project includes a Postman collection (`qr_code_scann.postman_collection.json`) with organized folders:

- **Collection** → Main API requests for `/items/`, `/scans/`
- **Error cases** → Invalid paths and missing data (422, 404 responses)
- **Negative cases** → Wrong relationships, empty strings, invalid inputs

### How to use
1. Open Postman.
2. Import `qr_code_scann.postman_collection.json`.
3. Run requests inside each folder:
   - **Collection** → Happy path CRUD operations.
   - **Error cases** → Verify error handling.
   - **Negative cases** → Test invalid inputs and relationships.


## 📜 License
This project is licensed under the MIT License.

## Author
Made by Ondina Hernandez— Software Tester Portfolio Project