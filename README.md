## Dependencies
It is always a good idea to use a virtual environment to isolate your python projects from your main environment!<br>

Install all runtime required dependencies using: `pip3 install -r requirements.txt` <br>
Install all runtime required dependencies and development dependencies using: `pip3 install -r dev_requirements.txt` <br>

## Unit tests with coverage reports
Run unit tests with coverage api using: `python3 -m coverage run -m unittest discover test` <br>
Generate a coverage report after testing using: `python3 -m coverage report` <br>

## Type checking
Run pyright with: `python3 -m pyright .`
