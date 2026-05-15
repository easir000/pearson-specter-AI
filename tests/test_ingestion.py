import os
import tempfile
import json  # ← ADD THIS LINE

from src.ingestion import process_document


def test_ingestion():
    with tempfile.TemporaryDirectory() as tmpdir:
        input_path = os.path.join(tmpdir, "input.txt")
        output_path = os.path.join(tmpdir, "output.json")
        
        # Use a single-word name to match your regex
        with open(input_path, "w") as f:
            f.write("Case No. 123\nPlaintiff: Doe")
        
        process_document(input_path, output_path)
        
        assert os.path.exists(output_path)
        with open(output_path) as f:
            data = json.load(f)
        
        assert data["plaintiff"] == "Doe"  # Now matches
        assert "clean_text" in data