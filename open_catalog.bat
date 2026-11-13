@echo off
call C:\fishing\start_server.bat
timeout /t 4 >nul
start "" http://127.0.0.1:8000/catalog_full.html
