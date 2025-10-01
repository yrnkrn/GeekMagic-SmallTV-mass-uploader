# -*- coding: utf-8 -*-
# Bulk uploader for GeekMagic SmallTV Pro via HTTP
# Supports both GIF and JPG/JPEG files

import sys
from pathlib import Path
import requests

# -------- CONFIG --------
BASE_URL   = "http://192.168.0.117/doUpload?dir=/image/"
UPLOAD_DIR = Path("upload")

session = requests.Session()

def main():
    files = list(UPLOAD_DIR.glob("*.gif")) + \
            list(UPLOAD_DIR.glob("*.jpg")) + \
            list(UPLOAD_DIR.glob("*.jpeg"))

    if not files:
        print(f"No .gif/.jpg files found in {UPLOAD_DIR.resolve()}")
        sys.exit(1)

    total = len(files)
    width = len(str(total))

    print(f"Uploading {total} file(s) to {BASE_URL}")
    for idx, p in enumerate(files, start=1):
        with p.open("rb") as f:
            files_dict = {"update": (p.name, f)}
            r = session.post(BASE_URL, files=files_dict, timeout=30)
        ok = (r.status_code in (200, 201, 204)) or r.ok

        prefix = f"{idx:0{width}}/{total:0{width}}"
        if ok:
            print(f"{prefix} OK   {p.name} - {r.status_code}")
        else:
            print(f"{prefix} FAIL {p.name} - {r.status_code}")
            sys.exit(1)

if __name__ == "__main__":
    main()
