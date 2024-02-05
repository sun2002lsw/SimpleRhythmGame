@echo off

:: 그냥 마음 편하게 업데이트하고 시작
pip install --upgrade pip
pip install pygame
cls

:: 폴더 이동해서 게임 실행
cd %~dp0
cd .\리듬게임\

py main.py
echo.

:: 디버깅을 위해서 창을 켜놓고 있기
pause
