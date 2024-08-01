from flask import Flask
from secrets import token_urlsafe
from flask_bootstrap import Bootstrap5
from flask_wtf import CSRFProtect
from requests import get as requests_get
from bs4 import BeautifulSoup

app = Flask(__name__)
app.secret_key = token_urlsafe(16)

bootstrap = Bootstrap5(app)
csrf = CSRFProtect(app)

def remove_tags(soup):
    for data in soup(['style', 'script']):
        data.decompose()

    return ' '.join(soup.stripped_strings)

def fetch_transcript(id):
    print("Fetching transcript for", id)
    transcriptXML = requests_get(f"https://youtubetranscript.com/?server_vid2={id}")
    transcript = remove_tags(BeautifulSoup(transcriptXML.text, 'xml'))
    return transcript

from summarizer import routes