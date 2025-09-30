# -*- coding: utf-8 -*-
# Simple bulk uploader for GeekMagic SmallTV Pro via HTTP

import os, sys, mimetypes
from pathlib import Path
import requests

# -------- CONFIG --------
BASE_URL     = "http://192.168.0.117/doUpload?dir=/image/"
REFERER_PAGE = "http://192.168.0.117/image.html"
GIF_DIR      = Path("upload_gifs")   # relative to this script
FILE_FIELD   = "update"              # form field name

session = requests.Session()

def upload_one(path: Path):
    ctype, _ = mimetypes.guess_type(path.name)
    if not ctype:
        ctype = "application/octet-stream"
    with path.open("rb") as f:
        files = {FILE_FIELD: (path.name, f, ctype)}
        r = session.post(BASE_URL, files=files, timeout=60)
    ok = (r.status_code in (200, 201, 204)) or r.ok
    print(("OK  " if ok else "FAIL"), path.name, "-", r.status_code)

def main():
    files = sorted(GIF_DIR.glob("*.gif"))
    if not files:
        print(f"No .gif files found in {GIF_DIR.resolve()}")
        sys.exit(1)

    print(f"Uploading {len(files)} GIF(s) to {BASE_URL}")
    for p in files:
        upload_one(p)

if __name__ == "__main__":
    main()
