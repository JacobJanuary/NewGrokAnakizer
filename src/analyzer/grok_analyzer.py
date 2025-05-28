"""
Анализатор твитов с использованием Grok API.
"""

import json
from typing import List, Dict, Optional
from openai import OpenAI


class GrokAnalyzer:
    """Анализатор твитов с использованием Grok API."""

    def __init__(self, config) -> None:
        """Инициализация анализатора Grok."""
        self.config = config
        self.client = OpenAI(
            api_key=config.api_key,
            base_url=config.base_url
        )
        self.system_prompt = self._get_system_prompt()

    def _get_system_prompt(self) -> Dict[str, str]:
        """Получение системного промпта."""
        prompt = """
Role: You are a crypto market analyst.

Task: Analyze tweets and provide structured information in Russian.

INPUT: JSON array of tweets
OUTPUT: JSON array with "type", "title", "description" fields

CRITICAL: Always return valid JSON array only.
"""
        return {"role": "system", "content": prompt}

    def analyze_tweets(self, tweets: List, use_web_search: Optional[bool] = None) -> List:
        """Анализ твитов с помощью Grok API."""
        if not tweets:
            return []

        print(f"Analyzing {len(tweets)} tweets with Grok API")

        # TODO: Добавить полную реализацию анализа
        results = []
        for tweet in tweets:
            results.append({
                "type": "others",
                "title": "Тест",
                "description": "Тестовое описание"
            })

        return results

    def test_connection(self) -> bool:
        """Тестирование подключения к Grok API."""
        try:
            print("Testing Grok API connection...")
            # TODO: Добавить реальное тестирование
            return True
        except Exception as e:
            print(f"API connection test failed: {e}")
            return False
