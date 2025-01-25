# servicios-ciudadanos

Prerequisites

Operating System: Windows 7 or higher

Dependencies:

pyenv-win: For managing multiple Python versions.

pyenv-win-venv: For managing virtual environments.

Installation

1. Install pyenv-win

Open PowerShell and run:

Invoke-WebRequest -UseBasicParsing -Uri "https://raw.githubusercontent.com/pyenv-win/pyenv-win/master/pyenv-win/install-pyenv-win.ps1" -OutFile "$env:USERPROFILE\install-pyenv-win.ps1"; & "$env:USERPROFILE\install-pyenv-win.ps1"

After installation, restart your terminal and verify the installation:

pyenv --version

2. Install pyenv-win-venv

With pyenv-win installed, proceed to install pyenv-win-venv:

pip install pyenv-win-venv

Setting Up the Python Environment

1. Install the Required Python Version

Replace 3.11.6 with the desired Python version:

pyenv install 3.11.6

2. Set the Local Python Version

Navigate to your project directory and set the local Python version:

cd C:\path\to\your\project
pyenv local 3.11.6

This command creates a .python-version file in your project directory specifying the Python version.

3. Create a Virtual Environment

Use pyenv-win-venv to create a virtual environment named .venv:

pyenv-venv create .venv

Activate the virtual environment:

pyenv-venv activate .venv

4. Install Project Dependencies

If you have a requirements.txt file, install the dependencies:

pip install -r requirements.txt

Usage

Provide instructions on how to run or use your project.

Updating pyenv-win

To update pyenv-win, run:

pyenv update

Troubleshooting

If you encounter issues:

Ensure that the pyenv-win paths are correctly set in your environment variables.

Verify that the correct Python version is active:

pyenv version

For detailed troubleshooting, refer to the pyenv-win FAQ.

Contributing

Provide guidelines for contributing to your project.

License

This project is licensed under the MIT License. See the LICENSE file for details.

