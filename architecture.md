# Architecture Overview

## System Goal
Generate grounded legal memos from messy inputs and improve from operator edits.

## Components
1. **Ingestion**: 
   - Simulates OCR cleanup
   - Extracts structured fields (case_id, plaintiff, etc.)
2. **Retrieval**: 
   - FAISS index over document text
   - Returns evidence with doc IDs for traceability
3. **Drafting**: 
   - Template-based memo with explicit evidence links
   - Zero external knowledge (fully grounded)
4. **Feedback**: 
   - Captures operator edits (original → corrected)
   - Retrains TF-IDF + Logistic Regression model
   - Flags low-confidence extractions for correction

## Grounding Guarantee
Every fact in the output cites a source doc ID. No hallucinations.

## Edit Loop
After 5+ edits, the system learns to auto-correct common OCR errors (e.g., "Jhon" → "John").