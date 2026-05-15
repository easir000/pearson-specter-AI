import json
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
import yaml

class EditLearner:
    def __init__(self):
        self.model = None
        self.vectorizer = TfidfVectorizer(max_features=100)
        self.edits = []
        with open("config.yaml") as f:
            self.config = yaml.safe_load(f)

    def capture_edit(self, original_fact: str, edited_fact: str, is_correction: bool):
        self.edits.append((original_fact, edited_fact, is_correction))

    def retrain(self):
        min_edits = self.config["feedback"]["min_edits_for_retrain"]
        if len(self.edits) < min_edits:
            return
        X = [orig for orig, _, _ in self.edits]
        y = [int(is_corr) for _, _, is_corr in self.edits]
        X_vec = self.vectorizer.fit_transform(X)
        self.model = LogisticRegression().fit(X_vec, y)

    def should_correct(self, fact: str) -> bool:
        if not self.model:
            return False
        threshold = self.config["feedback"]["correction_threshold"]
        vec = self.vectorizer.transform([fact])
        prob = self.model.predict_proba(vec)[0][1]
        return prob > threshold