# Build EXE script for whatshappeing

# Create virtual environment if it doesn't exist
if (!(Test-Path .venv)) {
    python -m venv .venv
}

# Activate virtual environment
.venv\Scripts\Activate.ps1

# Install dependencies
pip install -r requirements.txt

# Clean old builds
if (Test-Path build) { Remove-Item build -Recurse -Force }
if (Test-Path dist) { Remove-Item dist -Recurse -Force }

# Run PyInstaller
pyinstaller --onefile --windowed --name whatshappeing run.py

# Deactivate venv
deactivate