@echo off
REM Build script for creating a Windows executable of the Pygame platformer
REM This script runs PyInstaller with the game_build.spec configuration

echo ================================================
echo Building Pygame Platformer Executable
echo ================================================
echo.

REM Check if PyInstaller is available
pyinstaller --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: PyInstaller is not installed!
    echo Please install it first: pip install pyinstaller
    echo.
    pause
    exit /b 1
)

echo Using PyInstaller to build the executable...
echo.

REM Run PyInstaller with the spec file
pyinstaller game_build.spec

if errorlevel 1 (
    echo.
    echo ERROR: Build failed! Check the output above for errors.
    echo.
    pause
    exit /b 1
)

echo.
echo ================================================
echo Build completed successfully!
echo ================================================
echo.
echo The executable is located in: dist\main\
echo Run the game with: dist\main\main.exe
echo.
pause