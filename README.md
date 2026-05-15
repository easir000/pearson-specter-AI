# Pearson Specter AI Workflow

A production-grade system that ingests messy legal documents, extracts structured facts, generates grounded legal drafts, and improves from operator edits — all while ensuring full traceability and zero hallucinations.

Built to meet the core requirements:
1. **Document Processing** – Handles OCR errors and noisy inputs  
2. **Grounded Retrieval** – Evidence-linked RAG with FAISS  
3. **Draft Generation** – Structured, actionable legal memo  
4. **Improvement from Edits** – Real learning loop using operator feedback  

---

Here’s a **complete, step-by-step command-line guide** to set up, install dependencies, run your system, and execute tests for the **Pearson Specter Litt AI Engineer Take-Home Assessment** — optimized for **Windows (PowerShell)** but compatible with macOS/Linux.

---

### 🧰 **Step 1: Clone & Navigate to Project**
```powershell
# If starting fresh
git clone https://github.com/easir000/pearson-specter-ai.git
cd pearson-specter-ai
```

> ⚠️ **Important**: Make sure your repo **does NOT include `myenv/` or large binaries** (see `.gitignore` below).

---

### 📁 **Step 2: Create `.gitignore` (Critical!)**
Create `.gitignore` in your project root to exclude virtual environments and large files:

```gitignore
# Virtual environments
myenv/
venv/
env/

# Python cache
__pycache__/
*.pyc

# OS
.DS_Store
Thumbs.db

# Logs & data (optional)
*.log
data/processed/
```

Then clean Git history if needed:
```powershell
git rm -r --cached myenv/  # if already tracked
git add .gitignore
git commit -m "Exclude venv and large files"
```

---

### 🐍 **Step 3: Set Up Virtual Environment**
```powershell
# Create virtual environment
python -m venv myenv

# Activate it (Windows PowerShell)
myenv\Scripts\Activate.ps1

# On macOS/Linux, use:
# source myenv/bin/activate
```

You should see `(myenv)` in your prompt.

---

### 📦 **Step 4: Install Dependencies**
```powershell
pip install -r requirements.txt
```

✅ Expected output: Installs `faiss-cpu`, `sentence-transformers`, `scikit-learn`, `PyYAML`.

> 💡 If you get NumPy errors, run:
> ```powershell
> pip install "numpy==1.26.4"
> ```

---

### ▶️ **Step 5: Run the Main Pipeline**
```powershell
python -m src.main --input data/raw/case_001.txt --output output.json
```

✅ Expected output:
```
Processing document: data/raw/case_001.txt
Retrieving relevant evidence...
Generating draft memo...
✅ Done! Output saved to: output.json
```

Check `output.json`:
```json
{
  "facts": ["Plaintiff: Jhon", "Defendant: Acme"],
  "corrected_facts": ["Plaintiff: John", "Defendant: Acme"]
}
```

---

### 🧪 **Step 6: Run Tests**
First, install `pytest` (if not in `requirements.txt`):
```powershell
pip install pytest
```

Then run tests:
```powershell
python -m pytest tests/ -v
```

✅ Expected output:
```
tests/test_end_to_end.py::test_full_pipeline PASSED
tests/test_ingestion.py::test_ingestion PASSED
```

> 🔍 **Note**: Your `test_ingestion.py` must use a single-word name like `"Doe"` to match your regex.

---

### 🚀 **Step 7: Push to GitHub (Final)**
```powershell
git add .
git commit -m "Final submission: grounded legal AI pipeline with edit learning"
git push origin main
```

✅ No more `torch_cpu.dll` errors!

---

### 📝 **Summary of Key Commands**

| Task | Command |
|------|--------|
| **Activate venv** | `myenv\Scripts\Activate.ps1` |
| **Install deps** | `pip install -r requirements.txt` |
| **Run pipeline** | `python -m src.main --input data/raw/case_001.txt --output output.json` |
| **Run tests** | `python -m pytest tests/ -v` |
| **Push safely** | `git push origin main` |

---
