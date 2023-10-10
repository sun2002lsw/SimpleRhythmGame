@echo off

:: 그냥 마음 편하게 업데이트하고 시작
pip install --upgrade pip
pip install pygame
echo ====================

:: 폴더 이동해서 게임 실행
cd %~dp0
cd .\리듬게임\

python main.py
