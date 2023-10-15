@echo off

set /P title=작업 내용을 말하거라: 
echo.

cd %~dp0
git branch feature/edit-music-files master
git checkout feature/edit-music-files
git add -A && git commit -m "%title%"
echo.

git push --set-upstream origin feature/edit-music-files
echo.

:: 디버깅을 위해서 창을 켜놓고 있기
pause
