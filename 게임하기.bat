@echo off

:: �׳� ���� ���ϰ� ������Ʈ�ϰ� ����
pip install --upgrade pip
pip install pygame
cls

:: ���� �̵��ؼ� ���� ����
cd %~dp0
cd .\�������\

python main.py

:: ������� ���ؼ� â�� �ѳ��� �ֱ�
pause
