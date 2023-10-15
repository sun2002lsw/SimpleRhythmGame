@echo off

cd %~dp0

git fetch --all
echo.

git reset --hard origin/master
echo.

git checkout master
echo.

git pull
echo.
