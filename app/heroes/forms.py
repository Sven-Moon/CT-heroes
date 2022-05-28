from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, IntegerField, TextAreaField
from wtforms.validators import DataRequired, Length, NumberRange

class HeroForm(FlaskForm):    
    name = StringField('Name', validators=[DataRequired()])
    super_power = StringField('Super Power', validators=[DataRequired()])
    description = StringField('Description',validators=[Length(min=0,max=200)])
    comics_appeared_in = IntegerField('Number of Comics Appeared In', validators=[NumberRange(min=0)])
    image = StringField('Image Url')
    create = SubmitField('Create Hero')
    update = SubmitField('Update Hero')