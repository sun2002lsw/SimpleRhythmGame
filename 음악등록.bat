@echo off

set /P title=�۾� ������ ���ϰŶ�: 
echo.

cd %~dp0
git checkout -b feature/edit-music-files
git push --set-upstream origin feature/edit-music-files
cls

git add -A && git commit -m "%title%"
echo.
git push
echo.

:: ������� ���ؼ� â�� �ѳ��� �ֱ�
pause
