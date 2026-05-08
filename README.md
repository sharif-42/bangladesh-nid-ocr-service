# 🇧🇩 Bangladesh NID OCR Service

A **FastAPI-based OCR microservice** that extracts structured data from Bangladeshi National ID (NID) card images. Upload a photo of an NID card and get back clean, structured JSON containing bilingual names, parents' names, date of birth, and NID number.

Supports **dual AI backends** — switch between **OpenAI Vision** (cloud) and a **local LLM** (e.g., Ollama) with a single request parameter.

---

## ✨ Features

- **Image Upload → Structured JSON** — Upload an NID card image and receive parsed fields instantly
- **Dual AI Backend** — Choose between OpenAI Vision API or a local LLM (Ollama) per request
- **Bilingual Extraction** — Extracts both Bangla and English text from NID cards
- **Base64 Encoding** — Images are automatically encoded to base64 for LLM processing
- **Async Architecture** — Built with async/await for non-blocking I/O
- **Input Validation** — Validates file type and content before processing
- **Structured Error Handling** — Returns meaningful HTTP error codes (400, 401, 502, 500)
- **Pluggable Service Layer** — Abstract `OCRService` interface makes it easy to add new AI backends
- **Health Check Endpoint** — Built-in `/health` endpoint for monitoring

---

## 📋 Extracted Fields

| Field             | Description                                  | Example                        |
|-------------------|----------------------------------------------|--------------------------------|
| `name_bn`         | Full name in Bangla                          | `মোঃ শরিফুল ইসলাম`            |
| `name_en`         | Full name in English                         | `MD. SHARIFUL ISLAM`           |
| `father_name_bn`  | Father's full name in Bangla                 | `মোঃ XXXXX XXXXX`             |
| `mother_name_bn`  | Mother's full name in Bangla                 | `মোসাঃ XXXXX XXXXX`            |
| `date_of_birth`   | Date of birth as printed on the card         | `1 Jan 1900`                  |
| `nid_number`      | NID number as printed, preserving spaces     | `1234567890`                   |

---

## 🏗️ Architecture

```
app/
├── main.py                        # Application factory & health check
├── api/
│   └── v1/
│       └── routers/
│           └── nid.py             # POST /api/v1/extract-nid-info endpoint
├── core/
│   └── config.py                  # Pydantic settings (env-driven)
├── schemas/
│   └── nid.py                     # Request/Response Pydantic models
├── services/
│   ├── interfaces.py              # Abstract OCRService base class
│   ├── open_ai_api_service.py     # OpenAI Vision implementation
│   └── local_ai_service.py        # Local LLM implementation (WIP)
└── utils/
    └── utils.py                   # OCR prompt template
```

The service follows a **clean, layered architecture**:

1. **Router Layer** — Handles HTTP concerns (validation, file upload, error responses)
2. **Service Layer** — Encapsulates AI/OCR logic behind an abstract interface
3. **Schema Layer** — Defines request/response models with Pydantic
4. **Config Layer** — Manages environment-driven settings

---

## 🚀 Quick Start

### Prerequisites

- Python 3.12+
- An OpenAI API key (for cloud mode), **or**
- A local LLM server like Ollama (for local mode)

### 1. Clone & Setup

```bash
git clone https://github.com/sharif-42/bangladesh-nid-ocr-service.git
cd bangladesh-nid-ocr-service

# Create and activate virtual environment
python3 -m venv .venv
source .venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

### 2. Configure Environment

Create a `.env` file in the project root:

```env
# OpenAI API
OPENAI_API_KEY=your-openai-api-key-here
OPENAI_MODEL=gpt-4.1-mini

# Request timeout (seconds)
REQUEST_TIMEOUT_SECONDS=10

# Local AI (optional)
LOCAL_LLM_MODEL=ollama/qwen3-8b
LOCAL_LLM_API_KEY=
LOCAL_LLM_BASE_URL=http://localhost:8001
```

### 3. Run the Server

```bash
uvicorn app.main:app --reload
```

The API will be available at `http://127.0.0.1:8000`.

---

## 📡 API Reference

### `POST /api/v1/extract-nid-info`

Extract structured fields from an NID card image.

**Content-Type:** `multipart/form-data`

| Parameter      | Type     | Default | Description                                      |
|----------------|----------|---------|--------------------------------------------------|
| `image`        | `file`   | —       | **(Required)** NID card image file (JPEG, PNG, etc.) |
| `use_local_ai` | `bool`   | `true`  | `true` = local LLM, `false` = OpenAI Vision     |
| `is_front`     | `bool`   | `true`  | `true` = front side, `false` = back side         |

#### Example Request (cURL)

```bash
curl -X POST http://127.0.0.1:8000/api/v1/extract-nid-info \
  -F "image=@/path/to/nid-card.jpg" \
  -F "use_local_ai=false" \
  -F "is_front=true"
```

#### Example Response

```json
{
  "name_bn": "মোঃ শরিফুল ইসলাম",
  "name_en": "MD. SHARIFUL ISLAM",
  "father_name_bn": "মোঃ XXXXX XXXXX",
  "mother_name_bn": "মোসাঃ XXXXX XXXXXX",
  "date_of_birth": "1 Jan 1900",
  "nid_number": "1234567890"
}
```

### `GET /health`

Health check endpoint.

```bash
curl http://127.0.0.1:8000/health
```

```json
{ "status": "ok" }
```

---

## ⚠️ Error Responses

| Status Code | Scenario                                          |
|-------------|---------------------------------------------------|
| `400`       | Invalid file type or empty image                  |
| `401`       | OpenAI API key is invalid or missing              |
| `500`       | Internal server / parsing error                   |
| `502`       | OpenAI API service error                          |

---

## 🛠️ Tech Stack

### Core Dependencies

| Package | Version | Purpose |
|---------|---------|---------|
| [FastAPI](https://fastapi.tiangolo.com/) | 0.136.1 | Async web framework |
| [OpenAI Python SDK](https://github.com/openai/openai-python) | 2.35.1 | OpenAI Vision API client |
| [Pydantic](https://docs.pydantic.dev/) | 2.13.4 | Data validation & settings management |
| [Uvicorn](https://www.uvicorn.org/) | 0.46.0 | ASGI server |
| [python-dotenv](https://github.com/theskumar/python-dotenv) | 1.2.2 | Environment variable management |
| [python-multipart](https://github.com/Kludex/python-multipart) | 0.0.27 | File upload (multipart form) support |
| [httpx](https://www.python-httpx.org/) | 0.28.1 | Async HTTP client (used by OpenAI SDK) |

### All Dependencies

<details>
<summary>Full list from <code>requirements.txt</code> (click to expand)</summary>

```
annotated-doc==0.0.4
annotated-types==0.7.0
anyio==4.13.0
certifi==2026.4.22
click==8.3.3
distro==1.9.0
fastapi==0.136.1
h11==0.16.0
httpcore==1.0.9
httpx==0.28.1
idna==3.13
jiter==0.14.0
openai==2.35.1
pydantic==2.13.4
pydantic_core==2.46.4
python-dotenv==1.2.2
python-multipart==0.0.27
sniffio==1.3.1
starlette==1.0.0
tqdm==4.67.3
typing-inspection==0.4.2
typing_extensions==4.15.0
uvicorn==0.46.0
```

</details>

---

## 📄 License

This project is licensed under the **MIT License** — see the [LICENSE](LICENSE) file for details.

---

## 👤 Author

**Md. Shariful Islam** — [@sharif-42](https://github.com/sharif-42)