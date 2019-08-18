from flask import Flask
from flask_basicauth import BasicAuth
import secrets
import configparser


app = Flask(__name__, template_folder='templates')

CONFIG = configparser.ConfigParser()
CONFIG.read("config.ini")

app.config['BASIC_AUTH_USERNAME'] = CONFIG["LIVESTREAM"]["username"]
app.config['BASIC_AUTH_PASSWORD'] = CONFIG["LIVESTREAM"]["password"]

basic_auth = BasicAuth(app)

IMAGE_PATH = CONFIG["LIVESTREAM"]["path"]

app.config["SECRET_KEY"] = secrets.token_hex(16)
app.config['JSON_AS_ASCII'] = False

from routes.pages import *
