from typing import Dict, Any
import openai
import anthropic
from tenacity import retry, stop_after_attempt, wait_random_exponential

class AIServiceManager:
    def __init__(self, config: Dict[str, Any]):
        # 機密情報のマスキング処理が未実装
        self.openai_client = openai.OpenAI(api_key=config['openai']['api_key'])
        self.claude_client = anthropic.Anthropic(api_key=config['anthropic']['api_key'])
        self.local_model = None  # CodeBERTモデル

    @retry(wait=wait_random_exponential(min=1, max=60), stop=stop_after_attempt(3))
    def analyze_with_fallback(self, content: str) -> Dict[str, Any]:
        try:
            # GPT-4による分析
            result = self.gpt4_analyze(content)
        except Exception as e:
            try:
                # Claudeによるフォールバック
                result = self.claude_analyze(content)
            except Exception as e:
                # ローカルモデルによる最終フォールバック
                result = self.local_analyze(content)
        return result

    def gpt4_analyze(self, content: str) -> Dict[str, Any]:
        response = self.openai_client.chat.completions.create(
            model="gpt-4",
            messages=[{
                "role": "system",
                "content": "コードの言語特徴を分析してください。"
            }, {
                "role": "user",
                "content": content
            }]
        )
        return self._parse_gpt4_response(response)

    def claude_analyze(self, content: str) -> Dict[str, Any]:
        response = self.claude_client.messages.create(
            model="claude-3-opus-20240229",
            messages=[{
                "role": "user",
                "content": f"以下のコードを分析してください:\n\n{content}"
            }]
        )
        return self._parse_claude_response(response)

    def local_analyze(self, content: str) -> Dict[str, Any]:
        # CodeBERTによるローカル分析
        if self.local_model is None:
            from .generate_embeddings import EmbeddingGenerator
            self.local_model = EmbeddingGenerator()
        return self.local_model.analyze(content)
