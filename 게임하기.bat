@echo off
cd %~dp0

:: use virtual environment
call .\.venv\Scripts\activate

:: play game
cd .\�������\
python main.py
echo.

:: pause for debugging
pause
