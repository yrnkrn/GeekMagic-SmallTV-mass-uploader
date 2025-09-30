# -*- coding: utf-8 -*-
# Bulk uploader for GeekMagic SmallTV Pro via HTTP
# Supports both GIF and JPG/JPEG files
# Prints progress as 0001/0693 ...

import sys, mimetypes
from pathlib import Path
import requests

# -------- CONFIG --------
BASE_URL   = "http://192.168.0.117/doUpload?dir=/image/"
UPLOAD_DIR = Path("upload")   # relative to this script

session = requests.Session()

def upload_one(path: Path):
    ctype, _ = mimetypes.guess_type(path.name)
    if not ctype:
        ctype = "application/octet-stream"
    with path.open("rb") as f:
        files = {"update": (path.name, f, ctype)}
        r = session.post(BASE_URL, files=files, timeout=60)
    ok = (r.status_code in (200, 201, 204)) or r.ok
    return ok, r.status_code

def main():
    # Collect GIF, JPG, JPEG (no sorting)
    files = list(UPLOAD_DIR.glob("*.gif")) + \
            list(UPLOAD_DIR.glob("*.jpg")) + \
            list(UPLOAD_DIR.glob("*.jpeg"))

    if not files:
        print(f"No .gif/.jpg files found in {UPLOAD_DIR.resolve()}")
        sys.exit(1)

    total = len(files)
    width = len(str(total))  # padding width (e.g. 4 for 1000 files)

    print(f"Uploading {total} file(s) to {BASE_URL}")
    for idx, p in enumerate(files, start=1):
        ok, status = upload_one(p)
        prefix = f"{idx:0{width}}/{total:0{width}}"
        print(f"{prefix} {'OK  ' if ok else 'FAIL'} {p.name} - {status}")

if __name__ == "__main__":
    main()
