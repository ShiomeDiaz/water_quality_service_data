@echo off
IF NOT EXIST venv (
    python -m venv venv
)
call venv\Scripts\activate
pip install --upgrade pip
pip install -r requirements.txt
python dataservicio.py
