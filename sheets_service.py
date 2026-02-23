import os
import json
import bcrypt
import certifi
from datetime import datetime
from google.oauth2 import service_account
from googleapiclient.discovery import build
import httplib2

import google_auth_httplib2

# Scopes for Google Sheets API
SCOPES = ['https://www.googleapis.com/auth/spreadsheets']

class SheetsService:
    def __init__(self):
        env_id = os.getenv("SPREADSHEET_ID", "")
        self.spreadsheet_id = self._extract_id(env_id)
        self.credentials_path = "credentials.json"
        self.service = self._authenticate()

    def _extract_id(self, spreadsheet_id: str) -> str:
        """Extracts the ID from a full Google Sheets URL or returns the ID as is."""
        if spreadsheet_id and "spreadsheets/d/" in spreadsheet_id:
            # Extract between '/d/' and next '/'
            parts = spreadsheet_id.split("/d/")
            if len(parts) > 1:
                return parts[1].split("/")[0]
        return spreadsheet_id or ""

    def _authenticate(self):
        if not os.path.exists(self.credentials_path):
            print(f"Error: {self.credentials_path} not found.")
            return None
        
        try:
            creds = service_account.Credentials.from_service_account_file(
                self.credentials_path, scopes=SCOPES
            )
            # Create a custom http client that uses certifi for SSL
            http = httplib2.Http(ca_certs=certifi.where())
            # Authorize the http client with credentials
            authorized_http = google_auth_httplib2.AuthorizedHttp(creds, http=http)
            
            service = build('sheets', 'v4', http=authorized_http)
            return service
        except Exception as e:
            print(f"Authentication failed: {e}")
            return None

    def hash_password(self, password: str) -> str:
        salt = bcrypt.gensalt()
        return bcrypt.hashpw(password.encode('utf-8'), salt).decode('utf-8')

    def append_user(self, email: str, password: str, role: str):
        if not self.service:
            print("Google Sheets Service not initialized. Check credentials.json")
            return False
            
        hashed_pw = self.hash_password(password)
        created_at = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        values = [[email, hashed_pw, role, created_at]]
        body = {'values': values}
        
        try:
            self.service.spreadsheets().values().append(
                spreadsheetId=self.spreadsheet_id,
                range="Sheet1!A:D",
                valueInputOption="RAW",
                body=body
            ).execute()
            return True
        except Exception as e:
            print(f"Error appending user: {e}")
            return False

    def get_users(self):
        if not self.service:
            print("Google Sheets Service not initialized.")
            return []
            
        try:
            result = self.service.spreadsheets().values().get(
                spreadsheetId=self.spreadsheet_id,
                range="Sheet1!A:D"
            ).execute()
            
            rows = result.get('values', [])
            if not rows:
                return []
            
            # Skip header row
            users = []
            for row in rows[1:]:
                if len(row) >= 4:
                    users.append({
                        "email": row[0],
                        "role": row[2],
                        "created_at": row[3]
                    })
            return users
        except Exception as e:
            print(f"Error fetching users: {e}")
            return []
