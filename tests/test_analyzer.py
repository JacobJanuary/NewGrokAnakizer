"""
Тесты для модуля анализа Grok.
"""

import unittest
from unittest.mock import Mock, patch
import json
import pytest

from src.analyzer.grok_analyzer import GrokAnalyzer
from src.config.config_manager import GrokConfig
from src.database.models import Tweet, TweetAnalysis
from src.utils.exceptions import GrokAPIError


class TestGrokAnalyzer(unittest.TestCase):
    """Тесты анализатора Grok."""

    def setUp(self):
        """Настройка тестов."""
        self.grok_config = GrokConfig(
            api_key="test_key",
            model_name="grok-3",
            use_web_search=True
        )
        self.analyzer = GrokAnalyzer(self.grok_config)

    @patch('src.analyzer.grok_analyzer.OpenAI')
    def test_analyze_tweets_success(self, mock_openai):
        """Тест успешного анализа твитов."""
        # Настройка мока
        mock_response = Mock()
        mock_response.choices = [Mock()]
        mock_response.choices[0].message.content = json.dumps([
            {"type": "trueNews", "title": "Новость BTC", "description": "Bitcoin вырос на 5%."},
            {"type": "isSpam", "title": "", "description": ""}
        ])

        mock_client = Mock()
        mock_client.chat.completions.create.return_value = mock_response
        mock_openai.return_value = mock_client

        self.analyzer.client = mock_client

        # Тестовые данные
        tweets = [
            Tweet(id=1, url="https://twitter.com/test1", text="Bitcoin surged 5% today"),
            Tweet(id=2, url="https://twitter.com/test2", text="Buy our coin! 1000x returns!")
        ]

        # Выполнение теста
        results = self.analyzer.analyze_tweets(tweets)

        # Проверки
        self.assertEqual(len(results), 2)
        self.assertEqual(results[0].type, "trueNews")
        self.assertEqual(results[0].title, "Новость BTC")
        self.assertEqual(results[1].type, "isSpam")
        self.assertTrue(results[0].is_valuable)
        self.assertFalse(results[1].is_valuable)

    @patch('src.analyzer.grok_analyzer.OpenAI')
    def test_analyze_tweets_invalid_json(self, mock_openai):
        """Тест обработки невалидного JSON."""
        # Настройка мока с невалидным JSON
        mock_response = Mock()
        mock_response.choices = [Mock()]
        mock_response.choices[0].message.content = "This is not JSON"

        mock_client = Mock()
        mock_client.chat.completions.create.return_value = mock_response
        mock_openai.return_value = mock_client

        self.analyzer.client = mock_client

        tweets = [Tweet(id=1, url="https://twitter.com/test", text="Test tweet")]

        # Тест должен вызвать исключение
        with self.assertRaises(GrokAPIError):
            self.analyzer.analyze_tweets(tweets)

    @patch('src.analyzer.grok_analyzer.OpenAI')
    def test_analyze_tweets_with_json_extraction(self, mock_openai):
        """Тест извлечения JSON из ответа."""
        # Ответ с JSON внутри текста
        json_data = [{"type": "trueNews", "title": "Тест", "description": "Описание"}]
        response_text = f"Here is the analysis: {json.dumps(json_data)} That's all."

        mock_response = Mock()
        mock_response.choices = [Mock()]
        mock_response.choices[0].message.content = response_text

        mock_client = Mock()
        mock_client.chat.completions.create.return_value = mock_response
        mock_openai.return_value = mock_client

        self.analyzer.client = mock_client

        tweets = [Tweet(id=1, url="https://twitter.com/test", text="Test tweet")]
        results = self.analyzer.analyze_tweets(tweets)

        self.assertEqual(len(results), 1)
        self.assertEqual(results[0].type, "trueNews")

    def test_prepare_request_params_with_web_search(self):
        """Тест подготовки параметров с веб-поиском."""
        params = self.analyzer._prepare_request_params(use_web_search=True)

        self.assertIn("search_parameters", params)
        self.assertEqual(params["search_parameters"]["mode"], "auto")
        self.assertEqual(params["model"], "grok-3")

    def test_prepare_request_params_without_web_search(self):
        """Тест подготовки параметров без веб-поиска."""
        params = self.analyzer._prepare_request_params(use_web_search=False)

        self.assertNotIn("search_parameters", params)
        self.assertEqual(params["model"], "grok-3")