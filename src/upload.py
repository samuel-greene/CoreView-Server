import argparse
from core import upload_slide

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Upload a FIBI slide to the lab server.")
    parser.add_argument("file", help="The path to the image file you want to upload")
    parser.add_argument("--tag", default=None, help="The tag for this upload")
    
    args = parser.parse_args()
    upload_slide(args.file, args.tag)