from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, IntegerField
from wtforms.validators import DataRequired

class HeroForm(FlaskForm):    
    name = StringField('Name', validators=[DataRequired()])
    super_power = StringField('Super Power', validators=[DataRequired()])
    description = StringField('Description')
    comics_appeared_in = IntegerField('Number of Comics Appeared In')
    submit = SubmitField()