import sys
import os
import subprocess
from pathlib import Path


def run_command(command: list, description: str) -> bool:
    """
    Выполнение команды с выводом результата.
    
    Args:
        command: Команда для выполнения
        description: Описание команды
        
    Returns:
        True если команда выполнена успешно
    """
    print(f"\n=== {description} ===")
    try:
        result = subprocess.run(command, check=True, capture_output=True, text=True)
        print(result.stdout)
        if result.stderr:
            print("STDERR:", result.stderr)
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Failed: {e}")
        print("STDOUT:", e.stdout)
        print("STDERR:", e.stderr)
        return False
    except FileNotFoundError:
        print(f"❌ Command not found: {command[0]}")
        return False


def main():
    """Главная функция запуска тестов."""
    # Переходим в корневую директорию проекта
    project_root = Path(__file__).parent.parent
    os.chdir(project_root)
    
    print("🧪 Running Crypto News Analyzer Tests")
    print(f"Working directory: {os.getcwd()}")
    
    all_passed = True
    
    # 1. Проверка кодового стиля с black
    if not run_command(
        ["python", "-m", "black", "--check", "--diff", "src/", "tests/", "scripts/"],
        "Code Style Check (Black)"
    ):
        print("💡 Run 'python -m black src/ tests/ scripts/' to fix formatting")
        all_passed = False
    
    # 2. Линтинг с flake8
    if not run_command(
        ["python", "-m", "flake8", "src/", "tests/", "scripts/"],
        "Linting (Flake8)"
    ):
        all_passed = False
    
    # 3. Проверка типов с mypy
    if not run_command(
        ["python", "-m", "mypy", "src/"],
        "Type Checking (MyPy)"
    ):
        all_passed = False
    
    # 4. Запуск unit тестов
    if not run_command(
        ["python", "-m", "pytest", "tests/", "-v", "--tb=short"],
        "Unit Tests (Pytest)"
    ):
        all_passed = False
    
    # 5. Тесты покрытия кода
    if not run_command(
        ["python", "-m", "pytest", "tests/", "--cov=src", "--cov-report=term-missing"],
        "Coverage Tests"
    ):
        all_passed = False
    
    # 6. Проверка безопасности (опционально, если установлен bandit)
    try:
        subprocess.run(["python", "-m", "bandit", "--version"], 
                      check=True, capture_output=True)
        if not run_command(
            ["python", "-m", "bandit", "-r", "src/", "-f", "text"],
            "Security Check (Bandit)"
        ):
            print("⚠️  Security issues found, but not blocking")
    except (subprocess.CalledProcessError, FileNotFoundError):
        print("ℹ️  Bandit not installed, skipping security check")
    
    # Результат
    print("\n" + "="*50)
    if all_passed:
        print("✅ All tests passed!")
        return 0
    else:
        print("❌ Some tests failed!")
        return 1


if __name__ == "__main__":
    sys.exit(main())