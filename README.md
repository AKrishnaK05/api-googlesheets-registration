# FastAPI User Registration with Google Sheets

A production-ready FastAPI application that uses Google Sheets as a database for user registration.

## 🚀 Features

- **FastAPI Backend**: Efficient and modern asynchronous API.
- **Google Sheets Integration**: Uses the Google Sheets V4 API for persistent storage.
- **Secure Hashing**: Passwords are never stored as plain text (uses `bcrypt`).
- **Modern UI**: A sleek, dark-themed responsive frontend built with Vanilla CSS.
- **SSL Compatibility**: Specifically configured to handle SSL/CA certificate issues on Windows using `certifi`.

## 🛠️ Architecture

- **`main.py`**: FastAPI application and endpoints.
- **`sheets_service.py`**: Google Sheets API logic & Authentication.
- **`models.py`**: Pydantic data validation schemas.
- **`static/index.html`**: Single-page frontend using JS `fetch()`.

## ⚙️ Setup Instructions

### 1. Google Sheets Setup
1. Create a Google Cloud Project and enable the **Google Sheets API**.
2. Create a **Service Account**, download the `credentials.json`, and place it in the project root.
3. Create a new Google Sheet and **Share** it with the service account email (as Editor).
4. Note the **Spreadsheet ID** from the URL: `https://docs.google.com/spreadsheets/d/SPREADSHEET_ID/edit`.

### 2. Installation
```bash
pip install -r requirements.txt
```

### 3. Environment Variables
You need to set your Spreadsheet ID as an environment variable:

**PowerShell:**
```powershell
$env:SPREADSHEET_ID = "your_spreadsheet_id_here"
```

**Bash:**
```bash
export SPREADSHEET_ID="your_spreadsheet_id_here"
```

### 4. Running the App
```bash
python main.py
```
Visit `http://localhost:8000` to register users.

## ⚠️ Troubleshooting (SSL Issues)
If you encounter `SSL: CERTIFICATE_VERIFY_FAILED` errors (common in some network/corporate environments), run the app with SSL verification disabled:

**PowerShell:**
```powershell
$env:VERIFY_SSL = "false"
python main.py
```

## 🔒 Security Note
The `credentials.json` is excluded from Git via `.gitignore`. Never commit your private keys to a public repository.
