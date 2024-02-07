@echo off
cd %~dp0

:: use virtual environment for pygame
call .\.venv\Scripts\activate

:: move working directory
cd .\simpleRhythmGame\

:: play game on python 3.11
python main.py
echo.

:: pause for debugging
pause
