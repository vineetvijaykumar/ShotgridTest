
# 🎬 ShotGrid Query & Display Tool

This project is a coding challenge solution that connects to LAIKA's ShotGrid demo site, queries project data, and renders the results as an HTML table using Flask.

## 📌 Features

- Connects to ShotGrid using the Python API (v3.6.2)
- Queries Sequences and their associated Shots
- Evaluates dynamic query fields per entity
- Renders results in a user-friendly HTML table
- Includes unit tests with mocked ShotGrid responses

---

## 🚀 Getting Started

### 1. Clone the Repo

```bash
git clone https://github.com/your-username/ShotgridTest.git
cd ShotgridTest
```

### 2. Set Up the Environment

```bash
python3.11 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

> ✅ Python 3.11 is recommended for compatibility.

---

### 3. Run the Flask App

```bash
python app.py
```

Then open your browser to:  
📍 `http://127.0.0.1:5000/`

---

## 🧪 Running Tests

Unit tests are located in the `tests/` folder and mock all external API calls.

```bash
pytest
```

To check test coverage (if using `pytest-cov`):

```bash
pytest --cov=query_utils
```

---

## ⚙️ Configuration

No `.env` file is required for this challenge. ShotGrid credentials and settings are defined directly for this test project:

- **Site**: `https://laika-demo.shotgunstudio.com`
- **Script Name**: `code_challenge`
- **API Key**: `2Drsqmdcfhjvfcv%kvxdaqvft`
- **Project ID**: `85`

> ⚠️ This is a demo project only. Credentials are safe for temporary public use as provided.

---

## 📁 Project Structure

```
ShotgridTest/
│
├── app.py                # Flask entrypoint
├── sg_connection.py      # ShotGrid API setup
├── query_utils.py        # Reusable query functions
├── templates/
│   └── table.html        # HTML rendering template
├── tests/
│   └── test_queries.py   # Unit tests with mocking
├── requirements.txt
└── .gitignore
```

---

## 📝 Notes

- Written with modularity and testability in mind
- Compliant with PEP8 formatting
- Uses ShotGrid v3.6.2 Python API

---

## 🧠 Author

Vineet Vijaykumar  
https://github.com/vineetvijaykumar/

---

## 🏁 License

This project is a coding challenge submission and is not intended for production use.
