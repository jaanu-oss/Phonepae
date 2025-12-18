"""
Setup script for PhonePe Pulse Analysis Project
"""

import subprocess
import sys
import os


def install_requirements():
    """Install all required packages"""
    print("📦 Installing required packages...")
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"])
        print("✅ All packages installed successfully!")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Error installing packages: {e}")
        return False


def create_directories():
    """Create necessary directories"""
    dirs = ['data', 'scripts', 'outputs']
    for dir_name in dirs:
        os.makedirs(dir_name, exist_ok=True)
    print("✅ Directories created!")


if __name__ == "__main__":
    print("\n" + "="*60)
    print("🚀 PhonePe Pulse Analysis - Setup")
    print("="*60 + "\n")
    
    create_directories()
    
    if install_requirements():
        print("\n" + "="*60)
        print("✅ Setup complete! You can now run: python main.py")
        print("="*60 + "\n")
    else:
        print("\n" + "="*60)
        print("⚠️  Setup encountered errors. Please check the output above.")
        print("="*60 + "\n")

