from flask import render_template, redirect, url_for
import g4f
from summarizer import URLForm
from summarizer import app, fetch_transcript

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