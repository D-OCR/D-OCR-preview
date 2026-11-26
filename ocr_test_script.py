import json
import os
import sys
from pathlib import Path
    
import requests
from dotenv import load_dotenv
    
API_URL = "http://localhost:8000/v1/ocr"
    
    # Load the .env that sits next to this script (utf-8-sig tolerates a BOM)
load_dotenv(Path(__file__).with_name(".env"), encoding="utf-8-sig")
    
    
def read_api_key() -> str:
        keys = os.getenv("OCR_API_KEYS")
        if not keys:
            sys.exit("OCR_API_KEYS not found in .env or environment")
        return keys.split(",")[0].strip()
    
    
def main() -> None:
        if len(sys.argv) < 2:
            sys.exit("Usage: python ocr_test_script.py <image-or-pdf> [output.json]")
    
        file_path = Path(sys.argv[1])
        out_path = Path(sys.argv[2] if len(sys.argv) > 2 else "ocr-result.json")
        if not file_path.is_file():
            sys.exit(f"File not found: {file_path}")
    
        with file_path.open("rb") as f:
            resp = requests.post(
                API_URL,
                headers={"X-API-Key": read_api_key()},
                files={"image": (file_path.name, f)},
                timeout=1800,  # CPU inference can be slow
            )
    
        print(f"HTTP {resp.status_code}")
        if not resp.ok:
            sys.exit(resp.text)
    
        out_path.write_text(
            json.dumps(resp.json(), ensure_ascii=False, indent=2), encoding="utf-8"
        )
        print(f"Saved response to {out_path}")
    
    
if __name__ == "__main__":
        main()
