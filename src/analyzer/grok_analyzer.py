"""
Анализатор твитов с использованием Grok API.
"""

import json
import time
from typing import List, Dict, Any, Optional

from openai import OpenAI

from ..config.config_manager import GrokConfig
from ..database.models import Tweet, TweetAnalysis
from ..utils.exceptions import GrokAPIError, ValidationError
from ..utils.logger import get_logger


class GrokAnalyzer:
    """Анализатор твитов с использованием Grok API."""

    def __init__(self, config: GrokConfig) -> None:
        """
        Инициализация анализатора Grok.

        Args:
            config: Конфигурация Grok API
        """
        self.config = config
        self.logger = get_logger(__name__)

        self.client = OpenAI(
            api_key=config.api_key,
            base_url=config.base_url
        )

        self.system_prompt = self._get_system_prompt()

    def _get_system_prompt(self) -> Dict[str, str]:
        """Получение системного промпта для анализа."""
        crypto_prompt = """
Role:
You are a highly experienced crypto market analyst with a proven track record in leading crypto media and research firms. Your expertise includes:
- Deep understanding of blockchain technology and crypto projects
- Ability to distinguish significant news from noise
- Skill in extracting key information from data streams
- Experience in technical analysis of crypto charts
- Knowledge of market psychology and trader behavior
- Ability to detect manipulation and misinformation

Task:
Analyze English-language tweets from crypto influencers and provide structured information in Russian for investment decision-making.

INPUT FORMAT
A JSON array of raw, unprocessed tweets:
[{"text": "tweet_text1"}, {"text": "tweet_text2"}, ...]

OUTPUT FORMAT
A JSON array where each object corresponds to one tweet and contains:
- "type": tweet category
- "title": concise Russian headline (3–5 words)
- "description": brief Russian summary (2–3 sentences)

ANALYSIS ALGORITHM

STEP 0: Duplicate Check
- For each tweet, check if it describes the same event as any previous tweet in the array (e.g., both mention XRP surpassing USDT in market cap).
- If so, return:
{"type": "alreadyPosted", "title": "", "description": ""}
- Do not analyze further.

STEP 1: Quality and Relevance Filter
- If the tweet is purely promotional, spam, or lacks meaningful content (see detailed criteria below), return:
{"type": "isSpam", "title": "", "description": ""}
- Criteria for spam/irrelevance:
    - Contains advertising, referral, or promotional material; calls to retweet, like, follow, join chats, giveaways, airdrops, quick profit promises, NFT/token launches, or similar.
    - Lacks concrete information — only emotions, memes, greetings, thanks, off-topic chatter, or generic reactions ("to the moon!", "HODL", "soon", etc.).
    - Is just a link, a news headline, clickbait, rhetorical question, or personal conversation without facts, analysis, or new information.
    - Merely repeats or rephrases media headlines without meaningful details, facts, or context.
    - Does not provide new data, analysis, forecast, educational, or market-related value.
    - Duplicates the meaning of other tweets (merge similar news/events into a single entry).
    - Cannot impact the crypto market or provide insider information or sound technical analysis.
    - If the tweet describes a local crime, accident, or minor incident that does not affect the crypto market, industry trends, or asset prices, classify as isFlood.

STEP 2: Informational Value Check
- Exclude tweets about local crimes, accidents, or minor incidents unless they have direct, significant impact on the crypto market, asset prices, or industry-wide trends.
- Proceed only if the tweet contains at least one of the following:
    - Actual, market-moving news: launches, listings, hacks, partnerships, bans/permissions, regulatory decisions, major reports/lawsuits, policy changes, official investigations, etc.
    - Authoritative opinions or forecasts with specifics (well-reasoned, with data or context).
    - Market or fundamental analysis: stats, fund flows, trend analysis, institutional activity, liquidation levels, etc.
    - Technical analysis with explanation: levels, indicators, patterns, market signals — only if accompanied by reasoning.
    - Important insider information confirmed by data or trustworthy sources.
    - Valuable educational content about crypto markets, tools, or strategies (guides, explanations, step-by-step instructions).
- If none apply, return:
{"type": "isFlood", "title": "", "description": ""}

STEP 3: Content Classification
- Assign one of the following types:
    - "trueNews": verified news with sources (e.g., "Binance officially announces token X listing")
    - "fakeNews": unverified info, rumors (e.g., "Rumor: SEC to approve Bitcoin ETF soon")
    - "inside": insider information (e.g., "My source at company X reports upcoming partnership")
    - "tutorial": educational material (e.g., "How to set up MetaMask for Ethereum")
    - "analytics": technical analysis (e.g., "BTC forms double bottom on 4H chart")
    - "trading": trading idea (e.g., "Considering ETH entry at $1800")
    - "others": other valuable tweets not fitting above categories
- If ambiguous, prioritize: trueNews > inside > analytics > trading > tutorial > fakeNews > others

STEP 4: Title and Description Generation
- For valuable tweets:
    - Title: 2–3 words in Russian, reflecting the tweet's key info
    - Description: 2 sentences in Russian, expanding on the title and clearly conveying the tweet's essence (15 words maximum)
- Important:
    - Use professional crypto market terminology
    - State facts directly, without phrases like "the author says" or "the tweet reports"
    - Do not invent or infer information not present in the tweet
    - Convey the original meaning as accurately as possible
    - Always include the name of the project, token, or company mentioned in the tweet in the title and/or description. If multiple projects are mentioned, include all key names.

CRITICAL REQUIREMENTS:
1. ALWAYS return a valid JSON array
2. Each array element must be a valid JSON object with exactly these fields: "type", "title", "description"
3. Never include any text outside the JSON array
4. Never add explanations, comments, or additional text
5. Ensure proper JSON escaping for special characters
6. If you encounter an error, return an empty array: []

EXAMPLE OUTPUT:
[
    {"type": "trueNews", "title": "Листинг XRP", "description": "Binance объявила о листинге XRP. Торговля начнется завтра."},
    {"type": "isSpam", "title": "", "description": ""},
    {"type": "analytics", "title": "BTC дно", "description": "Bitcoin формирует двойное дно на 4-часовом графике. Возможен отскок."}
]
"""
        return {"role": "system", "content": crypto_prompt}


    def analyze_tweets(
            self,
            tweets: List,
            use_web_search: Optional[bool] = None,
            retry_count: int = 3
    ) -> List:
        """
        Анализ твитов с помощью Grok API.

        Args:
            tweets: Список твитов для анализа
            use_web_search: Использовать ли веб-поиск
            retry_count: Количество попыток при ошибке

        Returns:
            Список результатов анализа
        """
        if not tweets:
            return []

        # Импортируем исключения
        from ..utils.exceptions import GrokAPIError, ErrorCode, handle_exception

        # Подготавливаем данные для анализа
        tweet_data = [{"text": tweet.text if hasattr(tweet, 'text') else str(tweet)} for tweet in tweets]
        tweets_json = json.dumps(tweet_data, ensure_ascii=False)

        messages = [
            self.system_prompt,
            {"role": "user", "content": tweets_json}
        ]

        request_params = self._prepare_request_params(use_web_search)
        request_params["messages"] = messages

        print(f"Analyzing {len(tweets)} tweets with Grok API")

        # Повторные попытки при ошибках
        last_error = None
        for attempt in range(retry_count):
            try:
                start_time = time.time()

                response = self.client.chat.completions.create(**request_params)

                processing_time = time.time() - start_time
                print(f"API call completed in {processing_time:.2f}s")

                if not response.choices or not response.choices[0].message.content:
                    raise GrokAPIError(
                        "Empty response from Grok API",
                        code=ErrorCode.GROK_INVALID_RESPONSE
                    )

                response_content = response.choices[0].message.content.strip()

                # Парсим и валидируем ответ
                response_json = self._extract_json_from_response(response_content)
                results = self._validate_and_convert_results(response_json)

                print(f"Successfully analyzed {len(results)} tweets")

                # Дополняем результаты если их меньше чем твитов
                from ..database.models import TweetAnalysis
                while len(results) < len(tweets):
                    results.append(TweetAnalysis(type="others", title="", description=""))

                return results

            except Exception as e:
                last_error = e
                print(f"Attempt {attempt + 1} failed: {e}")

                if attempt < retry_count - 1:
                    sleep_time = 2 ** attempt  # Exponential backoff
                    print(f"Retrying in {sleep_time} seconds...")
                    time.sleep(sleep_time)

        # Если все попытки неудачны, преобразуем ошибку
        if isinstance(last_error, Exception):
            # Определяем код ошибки по типу
            if "timeout" in str(last_error).lower():
                error_code = ErrorCode.GROK_TIMEOUT
            elif "connection" in str(last_error).lower():
                error_code = ErrorCode.GROK_CONNECTION_ERROR
            elif "rate limit" in str(last_error).lower():
                error_code = ErrorCode.GROK_RATE_LIMITED
            elif "quota" in str(last_error).lower():
                error_code = ErrorCode.GROK_QUOTA_EXCEEDED
            elif "auth" in str(last_error).lower() or "401" in str(last_error):
                error_code = ErrorCode.GROK_AUTH_FAILED
            else:
                error_code = ErrorCode.GROK_NETWORK_ERROR

            converted_error = GrokAPIError(
                f"Failed to analyze tweets after {retry_count} attempts: {last_error}",
                code=error_code,
                original_error=last_error,
                retry_possible=error_code in [ErrorCode.GROK_TIMEOUT, ErrorCode.GROK_NETWORK_ERROR,
                                              ErrorCode.GROK_RATE_LIMITED]
            )
            raise converted_error

        # Fallback на случай непредвиденной ошибки
        raise GrokAPIError(
            f"Failed to analyze tweets after {retry_count} attempts",
            code=ErrorCode.GROK_NETWORK_ERROR
        )

    def test_connection(self) -> bool:
        """
        Тестирование подключения к Grok API.

        Returns:
            True если подключение успешно
        """
        try:
            from ..utils.exceptions import GrokAPIError, ErrorCode

            print("Testing Grok API connection...")

            # Создаем тестовый твит
            test_tweet = type('TestTweet', (), {'text': 'Test connection to Grok API'})()

            # Простой тест запрос
            messages = [
                {"role": "system",
                 "content": "Return valid JSON array with one object: [{\"type\": \"test\", \"title\": \"Test\", \"description\": \"Test message\"}]"},
                {"role": "user", "content": "Test"}
            ]

            response = self.client.chat.completions.create(
                model=self.config.model_name,
                messages=messages,
                temperature=0.1,
                max_tokens=100,
                timeout=10  # Короткий таймаут для теста
            )

            if response.choices and response.choices[0].message.content:
                print("✓ Grok API connection successful")
                return True
            else:
                print("✗ Grok API returned empty response")
                return False

        except Exception as e:
            print(f"API connection test failed: {e}")
            return False

    def _prepare_request_params(self, use_web_search: bool = None) -> Dict[str, Any]:
        """Подготовка параметров запроса к API."""
        params = {
            "model": self.config.model_name,
            "temperature": self.config.temperature,
            "max_tokens": self.config.max_tokens,
        }

        # ИСПРАВЛЕНИЕ: Убираем неподдерживаемый параметр
        if use_web_search:
            print("⚠️  Web search not yet supported by current API version")

        return params

    def _extract_json_from_response(self, response_content: str) -> List[Dict[str, Any]]:
        """
        Извлечение JSON из ответа API.

        Args:
            response_content: Содержимое ответа

        Returns:
            Список словарей с результатами анализа
        """
        from ..utils.exceptions import GrokAPIError, ErrorCode

        try:
            response_json = json.loads(response_content)
        except json.JSONDecodeError as e:
            print(f"Initial JSON decode failed: {e}")

            # Попытка извлечь JSON из ответа
            json_start = response_content.find('[')
            json_end = response_content.rfind(']') + 1

            if json_start != -1 and json_end > json_start:
                try:
                    json_content = response_content[json_start:json_end]
                    response_json = json.loads(json_content)
                    print("Successfully extracted JSON from response")
                except json.JSONDecodeError:
                    print(f"Failed to extract JSON. Response sample: {response_content[:200]}...")
                    raise GrokAPIError(
                        f"Invalid JSON format in response: {e}",
                        code=ErrorCode.GROK_JSON_PARSE_ERROR,
                        response_data={"raw_response": response_content[:500]}
                    )
            else:
                print(f"No valid JSON array found. Response sample: {response_content[:200]}...")
                raise GrokAPIError(
                    f"No valid JSON found in response: {e}",
                    code=ErrorCode.GROK_JSON_PARSE_ERROR,
                    response_data={"raw_response": response_content[:500]}
                )

        if not isinstance(response_json, list):
            raise GrokAPIError(
                "Response is not a JSON array",
                code=ErrorCode.GROK_INVALID_RESPONSE,
                response_data={"response_type": type(response_json).__name__}
            )

        return response_json

    """
    Fix for GrokAnalyzer - Update the _validate_and_convert_results method to return TweetAnalysis objects instead of dictionaries.

    Replace the _validate_and_convert_results method in src/analyzer/grok_analyzer.py with this version:
    """

    def _validate_and_convert_results(self, response_json: List[Dict[str, Any]]) -> List:
        """
        Валидация и преобразование результатов анализа.
        """
        from ..database.models import TweetAnalysis

        results = []
        required_fields = ["type", "title", "description"]

        for i, item in enumerate(response_json):
            if not isinstance(item, dict):
                print(f"Item {i} is not a dictionary, skipping")
                continue

            # Проверяем и добавляем отсутствующие поля
            for field in required_fields:
                if field not in item:
                    print(f"Item {i} missing field '{field}', adding default")
                    item[field] = ""

            # Создаем объект TweetAnalysis
            try:
                analysis = TweetAnalysis(
                    type=str(item["type"]).strip(),
                    title=str(item["title"]).strip(),
                    description=str(item["description"]).strip()
                )
                results.append(analysis)
                print(f"Created TweetAnalysis object {i}: type={analysis.type}")
            except Exception as e:
                print(f"Failed to process item {i}: {e}")
                results.append(TweetAnalysis(type="others", title="", description=""))

        return results

    def analyze_single_tweet(self, tweet: Tweet, use_web_search: Optional[bool] = None) -> TweetAnalysis:
        """
        Анализ одного твита.

        Args:
            tweet: Твит для анализа
            use_web_search: Использовать ли веб-поиск

        Returns:
            Результат анализа
        """
        results = self.analyze_tweets([tweet], use_web_search)
        return results[0] if results else TweetAnalysis(type="others", title="", description="")

