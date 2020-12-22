@echo off
:: cd C:\Users\drx\Desktop\GH\GH\nginx-1.15.8
:: start nginx.exe
:: cd ..\
:: git pull
cd /d %~dp0
cd ..\nginx-1.15.8
start nginx.exe
cd ..\
git reset
git pull
