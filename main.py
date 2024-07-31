from flask import Flask, render_template, redirect, url_for
import g4f
import requests
from bs4 import BeautifulSoup
import secrets
from flask_bootstrap import Bootstrap5

from flask_wtf import FlaskForm, CSRFProtect
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired
import re

app = Flask(__name__)
app.secret_key = secrets.token_urlsafe(16)

bootstrap = Bootstrap5(app)
csrf = CSRFProtect(app)

class URLForm(FlaskForm):
    id = StringField('ID: ', validators=[DataRequired()])
    lang = StringField('Language: ', validators=[DataRequired()])
    model = StringField('Model (gpt-4o or gpt-3.5-turbo): ', validators=[DataRequired()])
    submit = SubmitField('Get Summary')

def remove_tags(soup):

    for data in soup(['style', 'script']):
        data.decompose()

    return ' '.join(soup.stripped_strings)

def fetch_transcript(id):
    print(id)
    transcriptXML = requests.get(f"https://youtubetranscript.com/?server_vid2={id}")
    transcript = remove_tags(BeautifulSoup(transcriptXML.text, 'lxml'))
    return transcript




@app.route('/', methods=['GET', 'POST'])
def main_page():
    form = URLForm()
    if form.validate_on_submit():
        id = form.id.data
        print(id)
        lang = form.lang.data
        print(lang)
        model = form.model.data
        print(model)
        return redirect(url_for('summary_page', id=id, lang=lang, model=model))


    return render_template('main_page.html', form=form)

@app.route('/get-summary/<id>/<lang>/<model>')
def summary_page(id, lang, model):
    print("Getting summary")
    

    prompt = f"""As a video script expert, write a video script with the topic {fetch_transcript(id)}
    You have three tasks, which are:
    1.to summarize the text I provided into a Summary .Please answer within 100-200 characters.
    2.to summarize the text I provided, using up to seven Highlight. Choose an appropriate emoji for each Highlight and place it at the end of each  Highlight.
    3.to summarize the text I provided, using up to seven Key Insights. Each insight should include a brief in-depth analysis. Choose appropriate emoji for each key insights.
    Choose an appropriate emoji for each Key Insight and place it at the end of each Key Insight. 
    Key Insight should not include timestamps.
    Your output should use the language {lang}
    and Using the following template strictly, provide the results for the three tasks:   
    ## Summary    
    ### Highlights    
    - emoji Highlights    
    ### Key Insights    
    - emoji Key Insights     
    You need to return in the {lang} language type.
    """

    response = g4f.ChatCompletion.create(
        model=model,
        messages=[{"role": "user", "content": prompt}],
    )

    return response

if __name__ == '__main__':
    from waitress import serve
    serve(app, host="0.0.0.0", port=8080)
