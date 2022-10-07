## facebook_friends

#### Overview

This program use a Chrome portable version to crawl a Facebook profile (only the available data).

#### Dependencies:

- Python 3.x ("https://www.python.org/downloads")

> OBS: on Windows, make sure to check the option "add Python to Windows PATH"

#### Running the program

- Windows

1. Run "install.bat".
2. After cmd window shutdown, run "facebook_friends.bat".
3. Follow the instructions on screen.

- Linux

Create and activate a virtual python environment:

	python3 -m venv venv
	source venv/bin/activate	

Install python dependencies:

	pip install -r requirements

Run the crawler:

	python facebook_friends.py

- Notes:

1. The program can be finished anytime pressing "ctrl" + "c"
2. The profiles may be crawled one by one avoiding Facebook's blocking.