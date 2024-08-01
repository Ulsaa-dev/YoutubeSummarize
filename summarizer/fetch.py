from requests import get as requests_get
from bs4 import BeautifulSoup

def remove_tags(soup):
    for data in soup(['style', 'script']):
        data.decompose()

    return ' '.join(soup.stripped_strings)

def fetch_transcript(id):
    print("Fetching transcript for", id)
    transcriptXML = requests_get(f"https://youtubetranscript.com/?server_vid2={id}")
    transcript = remove_tags(BeautifulSoup(transcriptXML.text, 'lxml'))
    return transcript