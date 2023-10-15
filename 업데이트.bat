@echo off

cd %~dp0

git fetch --all
git reset --hard origin/master
git pull
git checkout master
