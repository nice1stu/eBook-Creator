@echo off
setlocal
cd /d "%~dp0"
title eBook Converter Tester v2.5.1

echo ============================================================
echo        EBOOK CREATOR - SYSTEM DIAGNOSTICS
echo ============================================================
echo.
echo Checking environment...
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo [ERROR] Python not found.
    pause
    exit
)

echo.
echo Running Multi-Format and Metadata Test...
echo ------------------------------------------------------------
python tester.py
echo ------------------------------------------------------------
echo Test process complete.
pause