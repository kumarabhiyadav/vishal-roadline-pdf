@echo off
REM Navigate to backend folder
cd backend

REM Activate virtual environment (using call is important!)
call .venv\Scripts\activate.bat

REM Move back to root directory
cd ..

REM Run the main Python file
python main.py

REM Pause to keep window open after execution
pause
