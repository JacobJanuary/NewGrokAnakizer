"""
Модели данных для Crypto News Analyzer.
"""

from dataclasses import dataclass
from enum import Enum
from typing import Optional
from datetime import datetime


class TweetType(Enum):
    """Типы анализа твитов."""
    TRUE_NEWS = "trueNews"
    FAKE_NEWS = "fakeNews"
    INSIDE = "inside"
    TUTORIAL = "tutorial"
    ANALYTICS = "analytics"
    TRADING = "trading"
    OTHERS = "others"
    SPAM = "isSpam"
    FLOOD = "isFlood"
    ALREADY_POSTED = "alreadyPosted"


@dataclass
class Tweet:
    """Модель твита."""
    id: int
    url: str
    text: str
    created_at: Optional[datetime] = None
    is_grok_processed: Optional[bool] = None

    def __post_init__(self):
        """Пост-инициализация для валидации."""
        if not self.url:
            raise ValueError("Tweet URL cannot be empty")
        if not self.text:
            raise ValueError("Tweet text cannot be empty")


@dataclass
class TweetAnalysis:
    """Модель результата анализа твита."""
    type: str
    title: str
    description: str

    def __post_init__(self):
        """Пост-инициализация для валидации."""
        # Проверяем, что type является валидным значением
        valid_types = [t.value for t in TweetType]
        if self.type not in valid_types:
            raise ValueError(f"Invalid tweet type: {self.type}")

    @property
    def is_valuable(self) -> bool:
        """Проверка, является ли анализ ценным для публикации."""
        non_valuable_types = [TweetType.SPAM.value, TweetType.FLOOD.value, TweetType.ALREADY_POSTED.value]
        return self.type not in non_valuable_types and self.title and self.description

    @property
    def category(self) -> str:
        """Получение категории для группировки."""
        category_map = {
            TweetType.TRUE_NEWS.value: "news",
            TweetType.FAKE_NEWS.value: "rumors",
            TweetType.INSIDE.value: "inside",
            TweetType.TUTORIAL.value: "education",
            TweetType.ANALYTICS.value: "analytics",
            TweetType.TRADING.value: "trading",
            TweetType.OTHERS.value: "others"
        }
        return category_map.get(self.type, "others")


@dataclass
class AnalysisStats:
    """Статистика анализа."""
    total_tweets: int
    processed_tweets: int
    valuable_tweets: int
    spam_tweets: int
    flood_tweets: int
    duplicate_tweets: int
    error_count: int
    processing_time: float

    @property
    def success_rate(self) -> float:
        """Процент успешно обработанных твитов."""
        if self.total_tweets == 0:
            return 0.0
        return (self.processed_tweets / self.total_tweets) * 100

    @property
    def valuable_rate(self) -> float:
        """Процент ценных твитов."""
        if self.processed_tweets == 0:
            return 0.0
        return (self.valuable_tweets / self.processed_tweets) * 100