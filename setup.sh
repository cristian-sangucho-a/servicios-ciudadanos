#!/bin/bash
brew install zlib
export LDFLAGS="-L/usr/local/opt/zlib/lib"
export CPPFLAGS="-I/usr/local/opt/zlib/include"
pyenv install 3.12.5
pyenv local 3.12.5

pyenv exec  python -m venv .venv

pyenv exec pip install -r requirements.txt
