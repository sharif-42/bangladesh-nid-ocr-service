# bangladesh-nid-ocr-service
FastAPI service for extracting structured fields from Bangladeshi National ID card images using OpenAI Vision—returns clean JSON with Bangla and English names, parents’ names, date of birth, and NID number.

## Features

- Extracts key NID fields from uploaded card images
- Returns clean, structured JSON output
- Supports Bangla and English names

## Extracted Fields

- Name (Bangla)
- Name (English)
- Father's name
- Mother's name
- Date of birth
- NID number

## Quick Start

```bash
# create virtual environment
python3 -m venv venv
source .venv/bin/activate

# install dependencies
pip install -r requirements.txt

# run the API
uvicorn app.main:app --reload
```