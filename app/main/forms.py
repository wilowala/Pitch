from flask_wtf import FlaskForm
from wtforms import StringField,TextAreaField,SubmitField
from wtforms.validators import InputRequired

class PitchForm(FlaskForm):

    pitch_cartegory = StringField('Pitch Cartegoryt',validators=[InputRequired()])
    title = StringField('Pitch title',validators=[InputRequired()])
    pitch = TextAreaField('Pitch')
    submit = SubmitField('Submit')