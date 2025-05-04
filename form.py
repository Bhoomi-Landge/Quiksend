from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Length
from flask_wtf import FlaskForm
from form import RegistrationForm
class RegistrationForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(min=4, max=20)])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Sign Up')
