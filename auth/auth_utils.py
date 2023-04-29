from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, EqualTo
from flask_login import UserMixin, login_user
from werkzeug.security import check_password_hash
from flask import Flask, redirect, url_for


