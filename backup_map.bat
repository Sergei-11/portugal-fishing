@echo off
cd /d C:\fishing
set STAMP=%DATE:~-4%-%DATE:~3,2%-%DATE:~0,2%_%TIME:~0,2%-%TIME:~3,2%
set STAMP=%STAMP: =0%
if not exist _ROLLBACK_MAP mkdir _ROLLBACK_MAP
copy map_rescued.html "_ROLLBACK_MAP\map_rescued_%STAMP%.html" >nul
echo Backup: _ROLLBACK_MAP\map_rescued_%STAMP%.html
pause
