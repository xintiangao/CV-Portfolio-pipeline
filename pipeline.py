import os
import io
import json
from google.oauth2 import service_account
from googleapiclient.discovery import build
from googleapiclient.http import MediaIoBaseDownload

def download_google_doc(doc_id, service_account_info):
    print("Connecting to Google Drive API...")
    creds = service_account.Credentials.from_service_account_info(service_account_info)
    service = build('drive', 'v3', credentials=creds)
    
    request = service.files().export_media(
        fileId=doc_id, 
        mimeType='application/vnd.openxmlformats-officedocument.wordprocessingml.document'
    )
    
    fh = io.BytesIO()
    downloader = MediaIoBaseDownload(fh, request)
    done = False
    while not done:
        status, done = downloader.next_chunk()
        print(f"Download Progress: {int(status.progress() * 100)}%")
        
    with open("current-cv.docx", "wb") as f:
        f.write(fh.getvalue())
    print("CV downloaded successfully and saved as current-cv.docx")

if __name__ == "__main__":
    doc_id = os.environ.get("GOOGLE_DOC_ID")
    sa_json_str = os.environ.get("GOOGLE_SERVICE_ACCOUNT")
    
    if not doc_id or not sa_json_str:
        raise ValueError("Missing mandatory environment variables. Check GitHub Secrets.")
        
    sa_info = json.loads(sa_json_str)
    
    # 1. Fetch latest raw file from Google Drive
    download_google_doc(doc_id, sa_info)
    
    # 2. Trigger your existing parser scripts
    print("Executing custom CV parsing logic...")
    # =========================================================
    # YOUR PARSER INTERFACE HERE:
    # This should read current-cv.docx and overwrite files in your data/ folder
    # os.system("python your_existing_parse_script.py")
    # =========================================================
    
    print("Local parsing complete. Handing off deployment to Cloudflare Pages Action.")