@echo off
mshta "javascript:new ActiveXObject('WScript.Shell').Run('python.exe -m http.server 8000 --directory C:\fishing',0,false);close()"
