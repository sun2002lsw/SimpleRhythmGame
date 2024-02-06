@echo off
cd %~dp0

set /P title=작업 내용을 말하거라: 
echo.

:: create branch & checkout
git branch feature/edit-music-files master
echo.
git checkout feature/edit-music-files
echo.

:: commit & push
git add -A && git commit -m "%title%"
echo.
git push --set-upstream origin feature/edit-music-files
echo.

:: pause for debugging
pause
