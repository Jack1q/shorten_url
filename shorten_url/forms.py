from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import URL, DataRequired

class URLForm(FlaskForm):
    url = StringField(label="URL",validators=[DataRequired(), URL()] )
    submit = SubmitField('Shorten URL')