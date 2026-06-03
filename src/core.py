# fibi_core.py
from pydrive2.auth import GoogleAuth
from pydrive2.drive import GoogleDrive
import os

MASTER_FOLDER_ID = '0AJ2Har0iz1dkUk9PVA'

def authenticate():
    src_dir = os.path.dirname(os.path.abspath(__file__))
    
    root_dir = os.path.dirname(src_dir)
    
    settings_path = os.path.join(root_dir, "config", "settings.yaml")
    
    gauth = GoogleAuth(settings_file=settings_path)
    gauth.ServiceAuth()
    
    return GoogleDrive(gauth)

def upload_slide(filepath, upload_name):
    drive = authenticate()
    filename = os.path.basename(filepath)
    
    print(f"Connecting to FIBI Server... preparing to upload {filename}")
    
    # Create the file metadata
    if upload_name:
        file_metadata = {
            'title': f"{upload_name}_{filename}",
            'parents': [{'id': MASTER_FOLDER_ID}]
        }
    else:
        file_metadata = {
            'title': f"{filename}",
            'parents': [{'id': MASTER_FOLDER_ID}]
        }

    
    file = drive.CreateFile(file_metadata)
    file.SetContentFile(filepath)
    
    try:
        # The crucial addition: param={'supportsAllDrives': True}
        file.Upload(param={'supportsAllDrives': True})
        print(f"Success! {filename} is now on the server.")
        return file['id']
    except Exception as e:
        print(f"Upload failed. Error: {e}")
        return None

def download_slide(file_id, save_path):
    drive = authenticate()
    file = drive.CreateFile({'id': file_id})
    print(f"Downloading {file['title']}...")
    file.GetContentFile(save_path)
    print("Download complete.")