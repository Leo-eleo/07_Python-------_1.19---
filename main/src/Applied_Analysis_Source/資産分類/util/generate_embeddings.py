import torch
from transformers import AutoTokenizer, AutoModel
import numpy as np
from pathlib import Path
import pickle
from .language_patterns import LANGUAGE_PATTERNS

class EmbeddingGenerator:
    def __init__(self, model_name="microsoft/codebert-base"):
        self.tokenizer = AutoTokenizer.from_pretrained(model_name)
        self.model = AutoModel.from_pretrained(model_name)
        self.device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
        self.model.to(self.device)

    def generate_embeddings(self, samples_dir: Path, output_file: Path):
        embeddings = {}
        
        for language in LANGUAGE_PATTERNS.keys():
            sample_path = samples_dir / f"{language.lower()}_sample.txt"
            if sample_path.exists():
                with open(sample_path, 'r', encoding='utf-8') as f:
                    code = f.read()
                    embeddings[language] = self._get_embedding(code)

        output_file.parent.mkdir(parents=True, exist_ok=True)
        with open(output_file, 'wb') as f:
            pickle.dump(embeddings, f)

    def _get_embedding(self, code: str) -> np.ndarray:
        inputs = self.tokenizer(code, return_tensors="pt", 
                              truncation=True, max_length=512)
        inputs = {k: v.to(self.device) for k, v in inputs.items()}
        
        with torch.no_grad():
            outputs = self.model(**inputs)
        return outputs.last_hidden_state.mean(dim=1).cpu().numpy()

if __name__ == "__main__":
    base_dir = Path(__file__).parent.parent
    generator = EmbeddingGenerator()
    generator.generate_embeddings(
        samples_dir=base_dir / "language_samples",
        output_file=base_dir / "temp" / "language_embeddings.pkl"
    )
