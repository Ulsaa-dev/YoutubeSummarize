from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired

class URLForm(FlaskForm):
    id = StringField('ID: ', validators=[DataRequired()])
    lang = StringField('Language: ', validators=[DataRequired()])
    model = StringField('Model (gpt-4o or gpt-3.5-turbo): ', validators=[DataRequired()])
    submit = SubmitField('Get Summary')