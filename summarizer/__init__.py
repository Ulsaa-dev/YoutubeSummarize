from flask import Flask
from secrets import token_urlsafe
from flask_bootstrap import Bootstrap5

from flask_wtf import CSRFProtect

app = Flask(__name__)
app.secret_key = token_urlsafe(16)

bootstrap = Bootstrap5(app)
csrf = CSRFProtect(app)

from summarizer import forms
from summarizer import routes