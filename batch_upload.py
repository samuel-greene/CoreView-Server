import os
import shutil
from concurrent.futures import ThreadPoolExecutor, as_completed
from core import upload_slide

# local paths
WATCH_DIR = "./upload_queue"
DONE_DIR = "./completed_uploads"
UPLOAD_NAME = "batch_upload"

# Ensure the local directories exist
os.makedirs(WATCH_DIR, exist_ok=True)
os.makedirs(DONE_DIR, exist_ok=True)

def process_single_file(filename):
    source_path = os.path.join(WATCH_DIR, filename)
    
    file_id = upload_slide(source_path, UPLOAD_NAME)
    
    if file_id:
        destination_path = os.path.join(DONE_DIR, filename)
        shutil.move(source_path, destination_path)
        return f"Successfully uploaded and moved: {filename}"
    else:
        return f"FAILED to upload: {filename}"

def main():
    files_to_upload = [f for f in os.listdir(WATCH_DIR) if os.path.isfile(os.path.join(WATCH_DIR, f))]
    
    if not files_to_upload:
        print(f"No files found in the queue. Drag files into '{WATCH_DIR}' and try again!")
        input("\nPress Enter to close...")
        return

    print(f"Found {len(files_to_upload)} files. Starting upload...\n")

    with ThreadPoolExecutor(max_workers=4) as executor:
        # submit all upload jobs to the thread pool
        futures = {executor.submit(process_single_file, fname): fname for fname in files_to_upload}
        
        # wait for completion
        for future in as_completed(futures):
            result = future.result()
            print(result)

    print("\n---- All batch tasks processed! ----")
    input("\nPress Enter to close this window...")

if __name__ == "__main__":
    main()