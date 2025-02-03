# servicios-ciudadanos

Prerequisites

Operating System: Windows 7 or higherss

Installation

1. Install pyenv-win

Open PowerShell and run:

```Invoke-WebRequest -UseBasicParsing -Uri "https://raw.githubusercontent.com/pyenv-win/pyenv-win/master/pyenv-win/install-pyenv-win.ps1" -OutFile "$env:USERPROFILE\install-pyenv-win.ps1"; & "$env:USERPROFILE\install-pyenv-win.ps1"```

After installation, restart your -----Computer------ and verify the installation:

pyenv --version

2. Run the following commands
- pyenv install 3.12.5
- pyenv local 3.12.5
- pyenv exec python -m venv .venv
- pyenv exec pip install -r requirements.txt

3. Add the interpreteer for the new .venv
 python interpreter -> add interpreter -> select local interpreter -> select existing -> (The path of current project) servicios-ciudadanos\.venv\Scripts\python.exe