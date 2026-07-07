import os
import io
import json
import paramiko
from google.oauth2 import service_account
from googleapiclient.discovery import build
from googleapiclient.http import MediaIoBaseDownload

# ==================== CONFIGURATION REGION ====================
# List the exact files and asset tracks that need to be synced to xintiangao.com
FILES_TO_UPLOAD = [
    "index.html",
    "data/publications.json",
    "data/talks.json",
    "css/style.css",
    "js/main.js"
] 
# ==============================================================

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

def deploy_to_server():
    print("Initiating SSH connection to remote hosting server...")
    ssh_host = os.environ.get("SERVER_HOST")
    ssh_user = os.environ.get("SERVER_USER")
    ssh_key_path = os.path.expanduser("~/.ssh/id_rsa") 
    remote_dir = os.environ.get("SERVER_REMOTE_DIR")   

    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh.connect(hostname=ssh_host, username=ssh_user, key_filename=ssh_key_path)
    
    sftp = ssh.open_sftp()
    
    # Ensure remote directories exist before uploading files nested inside them
    for file in FILES_TO_UPLOAD:
        if os.path.exists(file):
            remote_path = os.path.join(remote_dir, file)
            remote_dirname = os.path.dirname(remote_path)
            
            # Create remote directory structure if it's missing (like 'data/')
            try:
                sftp.stat(remote_dirname)
            except IOError:
                print(f"Creating remote directory: {remote_dirname}")
                ssh.exec_command(f"mkdir -p {remote_dirname}")
            
            print(f"Uploading {file} -> {remote_path}...")
            sftp.put(file, remote_path)
        else:
            print(f"Warning: File {file} not found. Skipping.")
            
    sftp.close()
    ssh.close()
    print("Deployment completed successfully! xintiangao.com is updated.")

if __name__ == "__main__":
    doc_id = os.environ.get("GOOGLE_DOC_ID")
    sa_json_str = os.environ.get("GOOGLE_SERVICE_ACCOUNT")
    
    if not doc_id or not sa_json_str:
        raise ValueError("Missing mandatory environment variables. Check GitHub Secrets.")
        
    sa_info = json.loads(sa_json_str)
    
    # 1. Fetch latest raw file
    download_google_doc(doc_id, sa_info)
    
    # 2. Trigger your existing parser scripts
    print("Executing custom CV parsing logic...")
    # =========================================================
    # YOUR INTERFACE HERE:
    # os.system("python your_existing_parse_script.py")
    # =========================================================
    
    # 3. Ship to web host
    deploy_to_server()