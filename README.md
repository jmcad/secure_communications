# DAT510 Assigment 2 - Secure Communications
To test part 2, two flask apps are needed.
The scripts names are alice.py and bob.py:
```
export FLASK_APP=alice.py
flask run --host 127.0.0.1 --port 8000
```
Open up a new terminal and enter
```
export FLASK_APP=bob.py
flask run --host 127.0.0.1 --port 5000
```

The above should be done in the directory where alice.py and bob.py are.
