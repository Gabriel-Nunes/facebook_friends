echo creating virtual environment..
python -m venv venv

echo installing dependencies...
venv\Scripts\python.exe -m pip install --upgrade pip
venv\Scripts\pip.exe install -r requirements.txt