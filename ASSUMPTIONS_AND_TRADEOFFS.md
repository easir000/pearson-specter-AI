# Assumptions & Tradeoffs

## Assumptions
- Input documents contain structured fields (case_id, plaintiff, etc.) in predictable formats.
- Operator edits are consistent (e.g., "Jhon" → "John" appears repeatedly).
- Ground truth exists in source documents (no external knowledge needed).

## Tradeoffs
| Decision | Why |
|---------|------|
| Simulated OCR instead of Tesseract | Faster setup; avoids heavy dependencies for take-home |
| FAISS over pgvector/Pinecone | Lightweight, no managed service needed |
| LogisticRegression over LLM fine-tuning | Low-data regime; interpretable corrections |
| Template-based drafting | Ensures grounding; avoids hallucination risk |
| In-memory edit learning | Simple demo; production would use DB |

## Scope Boundaries
- Focused on **fact extraction**, not legal reasoning
- Simulated edits instead of real UI
- Single-document processing (not multi-doc)