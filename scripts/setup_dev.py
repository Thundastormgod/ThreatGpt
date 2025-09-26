#!/usr/bin/env python3
"""Development setup script for ThreatGPT."""

import subprocess
import sys
from pathlib import Path


def run_command(command: str, description: str) -> bool:
    """Run a command and return success status."""
    print(f"🔧 {description}...")
    try:
        subprocess.run(command, shell=True, check=True, cwd=Path.cwd())
        print(f"✅ {description} completed successfully")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ {description} failed: {e}")
        return False


def main():
    """Main setup function."""
    print("🚀 Setting up ThreatGPT development environment...")
    
    commands = [
        ("python -m pip install --upgrade pip", "Upgrading pip"),
        ("python -m pip install poetry", "Installing Poetry"),
        ("poetry install --with dev,test", "Installing dependencies"),
        ("poetry run pre-commit install", "Installing pre-commit hooks"),
        ("poetry run pre-commit run --all-files", "Running code quality checks"),
    ]
    
    all_success = True
    for command, description in commands:
        if not run_command(command, description):
            all_success = False
            break
    
    if all_success:
        print("\n🎉 Development environment setup completed successfully!")
        print("\nNext steps:")
        print("1. Copy .env.example to .env and configure your settings")
        print("2. Start developing with: poetry shell")
        print("3. Run tests with: pytest")
        print("4. Start the CLI with: threatgpt --help")
    else:
        print("\n❌ Setup failed. Please check the errors above.")
        sys.exit(1)


if __name__ == "__main__":
    main()