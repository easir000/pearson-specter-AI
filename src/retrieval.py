import faiss
import numpy as np
from sentence_transformers import SentenceTransformer

class EvidenceRetriever:
    def __init__(self, docs):
        self.docs = docs
        self.model = SentenceTransformer('all-MiniLM-L6-v2')
        self._build_index()

    def _build_index(self):
        texts = [d["clean_text"] for d in self.docs]
        embeddings = self.model.encode(texts)
        self.index = faiss.IndexFlatIP(embeddings.shape[1])
        faiss.normalize_L2(embeddings)
        self.index.add(embeddings.astype(np.float32))
        self.doc_ids = list(range(len(self.docs)))

    def retrieve(self, query: str, k=3):
        emb = self.model.encode([query])
        faiss.normalize_L2(emb)
        scores, idxs = self.index.search(emb.astype(np.float32), k)
        results = []
        for i, idx in enumerate(idxs[0]):
            doc = self.docs[idx]
            results.append({
                "doc_id": int(idx),
                "text": doc["clean_text"],
                "metadata": {k: v for k, v in doc.items() if k != "clean_text"},
                "score": float(scores[0][i])
            })
        return results