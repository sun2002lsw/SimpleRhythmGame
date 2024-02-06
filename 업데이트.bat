@echo off
cd %~dp0

:: update recent change
git checkout master
echo.
git pull
echo.

:: delete auto created branch
git reset --hard origin/master
echo.
git branch -D feature/edit-music-files
echo.

:: for git ide
git fetch --all
echo.
