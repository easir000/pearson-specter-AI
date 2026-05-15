import re
import json
import yaml
from pathlib import Path

def load_config():
    with open("config.yaml") as f:
        return yaml.safe_load(f)

def ocr_mock(raw_text: str) -> str:
    """Simulate OCR cleanup using config."""
    config = load_config()
    text = raw_text
    for bad, good in config["ingestion"]["ocr_replacements"].items():
        text = text.replace(bad, good)
    return re.sub(r"[^a-zA-Z0-9\s\.\,\-\(\)\:\;]", " ", text)

def extract_structured_fields(text: str) -> dict:
    """Extract case metadata using regex."""
    case_id = re.search(r"Case No\.\s*(\d+-\d+)", text)
    plaintiff = re.search(r"Plaintiff:\s*([A-Z][a-z]+)", text)
    defendant = re.search(r"Defendant:\s*([A-Z][a-z]+)", text)
    date = re.search(r"Filed:\s*(\d{4}-\d{2}-\d{2})", text)
    
    return {
        "case_id": case_id.group(1) if case_id else "UNKNOWN",
        "plaintiff": plaintiff.group(1) if plaintiff else "UNKNOWN",
        "defendant": defendant.group(1) if defendant else "UNKNOWN",
        "filed_date": date.group(1) if date else "UNKNOWN",
        "clean_text": ocr_mock(text).strip()
    }

def process_document(input_path: str, output_path: str):
    with open(input_path) as f:
        raw = f.read()
    structured = extract_structured_fields(raw)
    Path(output_path).parent.mkdir(parents=True, exist_ok=True)
    with open(output_path, "w") as f:
        json.dump(structured, f, indent=2)


       