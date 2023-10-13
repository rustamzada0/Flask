from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField
from wtforms.validators import DataRequired, Email, Length


class RegisterForm(FlaskForm):
    full_name = StringField(label='Full Name', validators=[DataRequired(), Length(min=3, max=50)])
    email = StringField(label='Email', validators=[DataRequired(), Email(), Length(max=50)])
    password = StringField(label='Password', validators=[DataRequired(), Length(min=8, max=255)])
    confirm_password = StringField(label='Password', validators=[DataRequired(), Length(min=8, max=255)])


class LoginForm(FlaskForm):
    email = StringField(label='Email', validators=[DataRequired(), Email(), Length(max=50)])
    password = StringField(label='Password', validators=[DataRequired(), Length(min=8, max=255)])


class ContactForm(FlaskForm):
    full_name = StringField(label='Full Name', validators=[DataRequired(), Length(min=3, max=50)])
    email = StringField(label='Email', validators=[DataRequired(), Email(), Length(max=50)])
    subject = TextAreaField(label='Subject', validators=[DataRequired()])
    message = TextAreaField(label='Message', validators=[DataRequired()])


class ReviewForm(FlaskForm):
    message = TextAreaField(label='Review', validators=[DataRequired()])


class SearchForm(FlaskForm):
    message = TextAreaField(label='Search')

