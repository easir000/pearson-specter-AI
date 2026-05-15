import argparse
import json
import os
from pathlib import Path

# Relative imports (for package execution)
from .ingestion import process_document
from .retrieval import EvidenceRetriever
from .drafting import generate_memo
from .feedback import EditLearner


def main():
    parser = argparse.ArgumentParser(
        description="Pearson Specter AI: Grounded Legal Memo Generator"
    )
    parser.add_argument("--input", required=True, help="Path to input .txt file in data/raw/")
    parser.add_argument("--output", required=True, help="Path to output JSON file")
    args = parser.parse_args()

    # Validate input
    if not os.path.exists(args.input):
        raise FileNotFoundError(f"Input file not found: {args.input}")

    # Set up paths
    input_path = Path(args.input)
    processed_dir = Path("data/processed")
    processed_dir.mkdir(parents=True, exist_ok=True)
    processed_path = processed_dir / f"{input_path.stem}.json"

    print(f"Processing document: {args.input}")
    process_document(str(args.input), str(processed_path))

    # Load structured document
    with open(processed_path, "r", encoding="utf-8") as f:
        doc = json.load(f)

    # Retrieve evidence
    print("Retrieving relevant evidence...")
    retriever = EvidenceRetriever([doc])
    evidence = retriever.retrieve("Summarize case facts", k=3)

    # Generate draft
    print("Generating draft memo...")
    memo = generate_memo("Case Fact Summary", evidence)

    # Simulate operator edits with BOTH positive and negative examples
    learner = EditLearner()
    # Positive examples (corrections)
    for _ in range(4):
        learner.capture_edit("Plaintiff: Jhon", "Plaintiff: John", True)
    # Negative example (no correction needed)
    learner.capture_edit("Defendant: Acme", "Defendant: Acme", False)  # unchanged = not a correction
    learner.retrain()

    # Apply corrections
    corrected_facts = []
    for fact in memo["facts"]:
        # For demo: always correct known OCR error
        if "Jhon" in fact:
            corrected_facts.append(fact.replace("Jhon", "John"))
        else:
            corrected_facts.append(fact)
    memo["corrected_facts"] = corrected_facts

    # Save output
    with open(args.output, "w", encoding="utf-8") as f:
        json.dump(memo, f, indent=2, ensure_ascii=False)

    print(f"✅ Done! Output saved to: {args.output}")


if __name__ == "__main__":
    main()