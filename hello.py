from flask import Flask, render_template, session, redirect, url_for, flash
from flask_bootstrap import Bootstrap
from flask_moment import Moment
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired

from datetime import datetime, timezone

import os
from dotenv import load_dotenv

#Define a form class
class NameForm(FlaskForm):
    name = StringField('What is your name?', validators=[DataRequired()]) #DataRequired ensures that the field is not empty
    submit = SubmitField('Submit')

#Initialize app and built in modules
app = Flask(__name__)
bootstrap = Bootstrap(app)
moment = Moment(app)

#Load secret key for WTF forms
load_dotenv()
app.config["SECRET_KEY"] = os.getenv("WTF_SECRET")

@app.route('/', methods=['GET', 'POST'])
def index():
    form = NameForm()
    if form.validate_on_submit():
        old_name = session.get('name')
        if old_name is not None and old_name != form.name.data:
            flash('Looks like you have changed your name!')
        session['name'] = form.name.data
        return redirect(url_for('index'))
    return render_template('index.html', current_time=datetime.now(timezone.utc), form=form, name=session.get('name'))

@app.route('/user/<name>')
def user(name):
    return render_template('user.html', name=name, current_time=datetime.now(timezone.utc))

@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404

@app.errorhandler(500)
def internal_server_error(e):
    return render_template('500.html'), 500

if __name__ == '__main__':
    app.run(debug=True)