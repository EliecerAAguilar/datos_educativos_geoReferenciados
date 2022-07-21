import sys
sys.path.insert(0,'/var/www/flask-app-p')

activation = '/home/semestral/.local/share/virtualenvs/flask-app-p-voUfBLEy/bin/activation.py'
with open(activation) as file:
    exec(file.read(),dict(__file__=activation))

from app import app as aplication
