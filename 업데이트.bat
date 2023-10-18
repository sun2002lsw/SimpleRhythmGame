@echo off

cd %~dp0

git checkout master
echo.

git pull
echo.

git reset --hard origin/master
echo.
