@echo off
echo "Navigating to Root Dir"
cd /d %~dp0
cd ..\..

if not exist pyproject.toml (
    echo "Error: pyproject.toml not found in the current directory."
    exit /b 1
) else (
    echo "pyproject.toml found. Continuing with the script."
)

echo "Clearing old `.venv`"
RD /S /Q .venv

echo "Creating new `.venv`"
python -m venv .venv
rem call .venv\Scripts\activate.bat

echo "Installing dependencies"
.venv\Scripts\python.exe -m pip install --upgrade pip
.venv\Scripts\python.exe -m pip install flit
.venv\Scripts\python.exe -m flit install --pth-file
