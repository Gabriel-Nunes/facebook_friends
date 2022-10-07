echo creating virtual environment..
python -m venv venv
venv\Scripts\activate

echo installing dependencies...
python -m pip install --upgrade pip
pip install -r requirements.txt