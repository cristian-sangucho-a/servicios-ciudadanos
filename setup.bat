@echo off
REM Install Python version using pyenv-win
pyenv install 3.12.5
pyenv local 3.12.5

REM Create and activate virtual environment
python -m venv .venv
call .venv\Scripts\activate

REM Install dependencies
pip install -r requirements.txt
