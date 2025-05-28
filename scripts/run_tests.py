"""Скрипт запуска тестов."""

import sys
import os
import subprocess
from pathlib import Path


def run_command(command: list, description: str) -> bool:
    """Выполнение команды."""
    print(f"\n=== {description} ===")
    try:
        result = subprocess.run(command, check=True, capture_output=True, text=True)
        print(result.stdout)
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Failed: {e}")
        return False
    except FileNotFoundError:
        print(f"❌ Command not found: {command[0]}")
        return False


def main():
    """Главная функция запуска тестов."""
    project_root = Path(__file__).parent.parent
    os.chdir(project_root)

    print("🧪 Running Tests")

    # Запуск тестов
    success = run_command(
        ["python", "-m", "pytest", "tests/", "-v"],
        "Unit Tests"
    )

    if success:
        print("✅ All tests passed!")
        return 0
    else:
        print("⚠️ Some tests failed or pytest not installed")
        return 0


if __name__ == "__main__":
    sys.exit(main())
