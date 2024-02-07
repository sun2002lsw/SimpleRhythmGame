@echo off
cd %~dp0

:: use virtual environment
call .\.venv\Scripts\activate

:: play game
cd .\리듬게임\
python main.py
echo.

:: pause for debugging
pause
