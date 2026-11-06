@echo off
cd /d "%~dp0"
where py >nul 2>nul && (py dialer_server.py) || (python dialer_server.py)
if errorlevel 1 (echo. & echo Python is needed. Install it free from python.org, check "Add to PATH", then run this again. & pause)
