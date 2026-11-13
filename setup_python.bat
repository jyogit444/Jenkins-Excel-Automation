@echo off
setlocal
cd /d "%~dp0" || exit /b 1
echo Creating Python virtual environment...
py -3 -m venv .venv
if errorlevel 1 (
  echo ERROR: Python 3 not found. Install Python from python.org, then retry.
  exit /b 1
)
echo Installing Excel dependency...
".venv\Scripts\python.exe" -m pip install -r requirements.txt
if errorlevel 1 exit /b 1
echo SUCCESS: Setup complete. You can now create your Jenkins job.
exit /b 0
