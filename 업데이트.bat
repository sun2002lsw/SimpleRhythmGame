@echo off

cd %~dp0

git checkout master
echo.

git pull
echo.

git reset --hard origin/master
echo.

git branch -D feature/edit-music-files
echo.

git fetch --all
echo.
