"""Setup script for Crypto News Analyzer."""

from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="crypto-news-analyzer",
    version="1.0.0",
    author="Your Name",
    author_email="your.email@example.com",
    description="Automated crypto news analysis with Grok AI",
    long_description=long_description,
    long_description_content_type="text/markdown",
    packages=find_packages(),
    classifiers=[
        "Development Status :: 4 - Beta",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
    ],
    python_requires=">=3.9",
    install_requires=[
        "mysql-connector-python>=8.2.0",
        "python-dotenv>=1.0.0",
        "openai>=1.12.0",
        "python-telegram-bot>=20.7",
        "typing-extensions>=4.8.0",
    ],
)
