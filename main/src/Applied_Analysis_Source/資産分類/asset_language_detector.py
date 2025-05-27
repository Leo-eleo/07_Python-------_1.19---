import os
import pandas as pd
from transformers import AutoTokenizer, AutoModel
import torch
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np
from typing import Dict, List, Any
import chardet
import re
import yaml
from pathlib import Path

from util.language_patterns import LANGUAGE_PATTERNS, COMMENT_PATTERNS
from util.ai_service import AIServiceManager
from util.data_source import DataSourceManager

class AssetLanguageDetector:
    def __init__(self, config_path: str = "config.yml"):
        self.base_dir = Path(__file__).parent
        self.log_dir = self.base_dir / 'logs'
        self.log_dir.mkdir(exist_ok=True)
        
        self.error_log = self.log_dir / 'detector_error.log'
        self.execution_log = self.log_dir / 'detector_execution.log'
        
        with open(self.base_dir / config_path, 'r', encoding='utf-8') as f:
            self.config = yaml.safe_load(f)
            
        self.tokenizer = AutoTokenizer.from_pretrained(self.config['model']['name'])
        self.model = AutoModel.from_pretrained(self.config['model']['name'])
        self.language_embeddings = self._load_language_embeddings()
        self.patterns = LANGUAGE_PATTERNS

        self.ai_service = AIServiceManager(self.config)
        self.data_source = DataSourceManager(self.config)

    def _load_language_embeddings(self):
        embedding_file = self.base_dir / 'temp' / 'language_embeddings.pkl'
        if not embedding_file.exists():
            from util.generate_embeddings import EmbeddingGenerator
            generator = EmbeddingGenerator()
            generator.generate_embeddings(
                self.base_dir / 'language_samples',
                embedding_file
            )
        
        import pickle
        with open(embedding_file, 'rb') as f:
            return pickle.load(f)

    def _is_comment(self, line: str) -> bool:
        return any(re.match(pattern, line) for pattern in COMMENT_PATTERNS['general'])

    def process_directory(self, input_dir: str, output_path: str) -> None:
        # ログ処理の実装が不十分
        # 仕様書に記載されている詳細なログ出力の実装が必要
        results = []
        for root, _, files in os.walk(input_dir):
            for file in files:
                if file.endswith(('.txt', '.cbl', '.jcl', '.asm', '.prc', '.cpy', '.for')):
                    file_path = os.path.join(root, file)
                    try:
                        result = self._process_file(file_path)
                        results.append(result)
                    except Exception as e:
                        print(f"Error processing {file_path}: {e}")

        df = pd.DataFrame(results)
        df.to_excel(output_path, sheet_name='資産分類結果', index=False)

        # 結果の保存
        self.data_source.save_result(results)
        
        # クラウドへのバックアップ
        self.data_source.upload_to_cloud(
            output_path,
            f"results/{Path(output_path).name}"
        )

    def _process_file(self, file_path: str) -> Dict[str, Any]:
        content = self._read_file(file_path)
        language_info = self.detect_language(content)
        line_info = self._count_lines(content)
        
        return {
            'ファイル名': os.path.basename(file_path),
            '格納フォルダ': os.path.dirname(file_path),
            '資産分類': language_info['language'],
            '類似度閾値': language_info['confidence'],
            '資産ID': os.path.splitext(os.path.basename(file_path))[0],
            '有効ステップ数': line_info['effective_lines'],
            'コメント数': line_info['comment_lines']
        }

    def _read_file(self, file_path: str) -> str:
        with open(file_path, 'rb') as f:
            raw_content = f.read()
            encoding = chardet.detect(raw_content)['encoding'] or 'utf-8'
        
        try:
            return raw_content.decode(encoding)
        except UnicodeDecodeError:
            return raw_content.decode('shift-jis', errors='ignore')

    def _count_lines(self, content: str) -> Dict[str, int]:
        lines = content.splitlines()
        total_lines = len(lines)
        comment_lines = sum(1 for line in lines if self._is_comment(line))
        
        return {
            'total_lines': total_lines,
            'comment_lines': comment_lines,
            'effective_lines': total_lines - comment_lines
        }

    def detect_language(self, content: str) -> Dict[str, Any]:
        # AIサービスによる分析
        ai_result = self.ai_service.analyze_with_fallback(content)
        
        # 仕様書では判定閾値が0.8と記載されているが、
        # configファイルから取得するように修正すべき
        if ai_result['confidence'] >= self.config['model']['threshold']:
            return ai_result
        
        # 従来のルールベース判定
        # コードのベクトル化
        code_vector = self._get_code_embedding(content)
        
        # 各言語との類似度計算
        similarities = {}
        for lang, embed in self.language_embeddings.items():
            sim = cosine_similarity(code_vector, embed)[0][0]
            similarities[lang] = sim
        
        # 最も類似度の高い言語を選択
        best_lang = max(similarities.items(), key=lambda x: x[1])
        
        threshold = self.config['model']['threshold']
        if best_lang[1] >= threshold:
            return {
                'language': best_lang[0],
                'confidence': float(best_lang[1])
            }
        
        # RAGでの判定が失敗した場合、ルールベースで判定
        for lang, rules in self.patterns.items():
            for pattern in rules['patterns']:
                if re.search(pattern, content):
                    return {
                        'language': lang,
                        'confidence': 1.0
                    }
        
        return {
            'language': 'UNKNOWN',
            'confidence': 0.0
        }

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("--input-dir", required=True)
    parser.add_argument("--output", required=True)
    parser.add_argument("--threshold", type=float, default=0.9)
    args = parser.parse_args()

    detector = AssetLanguageDetector()
    detector.process_directory(args.input_dir, args.output)
