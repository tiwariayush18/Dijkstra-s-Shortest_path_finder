@echo off
setlocal
cd /d "%~dp0"

py -m PyInstaller --version >nul 2>&1
if errorlevel 1 (
    echo PyInstaller is not installed.
    echo Install it with: py -m pip install -r requirements-build.txt
    exit /b 1
)

py -m PyInstaller --noconfirm --clean --onefile --windowed ^
    --name ShortestPathFinder ^
    --distpath dist --workpath build --specpath build ^
    shortest_path_find.py
if errorlevel 1 exit /b %errorlevel%

echo.
echo Build complete: dist\ShortestPathFinder.exe
