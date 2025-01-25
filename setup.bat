pyenv install 3.12.5
pyenv local 3.12.5

pyenv exec python -m venv .venv
call .venv\Scripts\activate

pip install -r requirements.txt
