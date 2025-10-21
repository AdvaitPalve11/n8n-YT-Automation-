@echo off
REM Quick Start Batch Script for STEM Video Automation
REM For Windows users who prefer .bat files

echo ================================================================================
echo 🎬 STEM Video Automation - Starting Server
echo ================================================================================
echo.
echo Server will start at: http://127.0.0.1:8000
echo API Documentation: http://127.0.0.1:8000/docs
echo.
echo Press Ctrl+C to stop the server
echo ================================================================================
echo.

python server.py

pause
