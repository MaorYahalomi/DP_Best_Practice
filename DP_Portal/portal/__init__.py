from flask import Flask

app = Flask(__name__)

from portal import routes
