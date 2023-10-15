@echo off

cd %~dp0
echo.

git fetch --all
echo.

git reset --hard origin/master
echo.

git pull
echo.
