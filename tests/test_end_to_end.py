def test_full_pipeline():
    import tempfile
    from src.main import main
    import json

    with tempfile.TemporaryDirectory() as tmp:
        input_file = f"{tmp}/input.txt"
        output_file = f"{tmp}/output.json"
        
        with open(input_file, "w") as f:
            f.write("Case No. 123\nPlaintiff: Jhon Doe")
        
        # Mock CLI args
        import sys
        original_argv = sys.argv
        sys.argv = ["", "--input", input_file, "--output", output_file]
        
        try:
            main()
        finally:
            sys.argv = original_argv
        
        with open(output_file) as f:
            result = json.load(f)
        
        assert "Plaintiff: John" in result["corrected_facts"]
        assert len(result["facts"]) == 1  # deduplicated