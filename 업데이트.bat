@echo off

cd %~dp0
echo.

git fetch --all
echo.

git reset --hard origin/master
echo.

git pull
echo.

git checkout master
echo.

:: 디버깅을 위해서 창을 켜놓고 있기
pause
