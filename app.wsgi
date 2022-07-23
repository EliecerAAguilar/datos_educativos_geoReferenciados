import sys
sys.path.insert(0,'/var/www/flask-app-p')

activate_this = '/home/semestral/.local/share/virtualenvs/flask-app-p-voUfBLEy/bin/activate_this.py'
with open(activate_this) as file:
    exec(file.read(),dict(__file__=activation))

from app import app as aplication
