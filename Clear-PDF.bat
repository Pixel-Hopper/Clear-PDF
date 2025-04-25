@echo off
rem Batch file to run the PDF cleaner script

rem Change to the directory where the batch file is located
cd /d "%~dp0"

rem Run the Python script
rem Make sure python is in your PATH, or provide the full path to python executable
python Clear-PDF.py

pause