# File server

Asynchronous file server that allows basic CRUD operations over files as well as execution in an isolated docker environment.
The files are stored plainly in a server folder defined in the settings file.

#### Run
```python path/to/src/framework/wsgi.py```

#### Settings
Change any desired settings in the file `settings.json` located in the repository directory. Those values are loaded to `src/framework/settings.py` when the server is launched.

#### Requirements
To install the requirements use ```pip -r requirements/*environment*.txt``` where *environment* is the desired file located in the requirements directory in the repository root. 
