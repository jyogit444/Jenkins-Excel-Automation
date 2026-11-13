@echo off
setlocal
cd /d "%~dp0" || exit /b 1
if not exist ".venv\Scripts\python.exe" (
  echo ERROR: Python environment missing. Run setup_python.bat first.
  exit /b 1
)
".venv\Scripts\python.exe" "update_records.py"
exit /b %errorlevel%
