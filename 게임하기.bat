@echo off

:: �׳� ���� ���ϰ� ������Ʈ�ϰ� ����
pip install --upgrade pip
pip install pygame
echo ====================

:: ���� �̵��ؼ� ���� ����
cd %~dp0
cd .\�������\

python main.py
