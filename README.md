#Flask

## How to run commands

**Install virtualenv:**
Make sure this is done to ensure there's no dependency hell going on

```python
python3 -m pip install --user virtualenv
```

**Create a virtual environment:**
Do this before you create the project in the project directory (or else there'll be conflicts/consequences)

```python
python3 -m venv env
```

**Activate/Deactivate virtual environment**:
This will vary based on OS (mine is mac) plus the directory the venv is installed in

```python
source env/bin/activate
deactivate
```

**Install package with pip:**
Once you clone the project, install the necessary dependencies using this command

```python
pip install -r requirements.txt
```

**Start command for flask:**
Start the app in production mode (so you don't get 10000 warnings, network or error codes in the command prompt)

```python
flask --app haemo run
```

**Debug command:**
Run this when making changes to the app, since it shows all the background/error/network operations + don't have to reload when making changes to the backend file

```python
flask --app haemo --debug run
```
