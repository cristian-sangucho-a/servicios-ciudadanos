#!/bin/bash
brew install zlib
export LDFLAGS="-L/usr/local/opt/zlib/lib"
export CPPFLAGS="-I/usr/local/opt/zlib/include"
pyenv install 3.12.5
pyenv local 3.12.5

python -m venv .venv
source .venv/bin/activate

pip install -r requirements.txt
