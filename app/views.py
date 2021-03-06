"""
Flask Documentation:     http://flask.pocoo.org/docs/
Jinja2 Documentation:    http://jinja.pocoo.org/2/documentation/
Werkzeug Documentation:  http://werkzeug.pocoo.org/documentation/

This file creates your application.
"""

from app import app
from flask import render_template, request, redirect, url_for,jsonify,g,session
from app import db

from flask.ext.wtf import Form 
from wtforms.fields import TextField, PasswordField,BooleanField # other fields include PasswordField 
from wtforms.validators import Required, Email
from app.models import Myprofile

from flask.ext.login import login_user, logout_user, current_user, login_required
from app import app, db, lm, oid
from app import oid, lm

class ProfileForm(Form):
     first_name = TextField('First Name', validators=[Required()])
     last_name = TextField('Last Name', validators=[Required()])
     user_name = TextField('User Name', validators=[Required()])
     password=PasswordField('Password',validators=[Required()])

class LoginForm(Form):
    user_name = TextField('User Name', validators=[Required()])
    password=PasswordField('Password',validators=[Required()])
    remember_me = BooleanField('remember_me', default=False)


@app.before_request
def before_request():
    g.user = current_user
    
###
# Routing for your application.
###
@app.route('/login', methods=['GET', 'POST'])
@oid.loginhandler
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user=Myprofile.query.get(form.user_name.data)
        if form.password.data==user.password:
            login_user(user)
            return redirect(url_for('home'))
  
    return render_template('login.html', 
                           title='Sign In',
                           form=form,
                           )
@app.route('/')
def home():
    """Render website's home page."""
    return render_template('home.html')

@app.route('/profile/', methods=['POST','GET'])
def profile_add():
    if request.method == 'POST':
        first_name = request.form['first_name']
        last_name = request.form['last_name']
        user_name = request.form['user_name']
        password=request.form['password']
        # write the information to the database
        newprofile = Myprofile(first_name=first_name,last_name=last_name,nickname=user_name,password=password)
        db.session.add(newprofile)
        db.session.commit()

        return "{} {} was added to the database".format(request.form['first_name'],request.form['last_name'])

    form = ProfileForm()
    return render_template('profile_add.html',
                           form=form)

@app.route('/profiles/',methods=["POST","GET"])
def profile_list():
    profiles = Myprofile.query.all()
    if request.method == "POST":
        return jsonify({"age":4, "name":"John"})
    return render_template('profile_list.html',
                            profiles=profiles)

@app.route('/profile/<int:id>')
def profile_view(id):
    profile = Myprofile.query.get(id)
    return render_template('profile_view.html',profile=profile)


@app.route('/about/')
def about():
    """Render the website's about page."""
    return render_template('about.html')


###
# The functions below should be applicable to all Flask apps.
###

@app.route('/<file_name>.txt')
def send_text_file(file_name):
    """Send your static text file."""
    file_dot_text = file_name + '.txt'
    return app.send_static_file(file_dot_text)


@app.after_request
def add_header(response):
    """
    Add headers to both force latest IE rendering engine or Chrome Frame,
    and also to cache the rendered page for 10 minutes.
    """
    response.headers['X-UA-Compatible'] = 'IE=Edge,chrome=1'
    response.headers['Cache-Control'] = 'public, max-age=600'
    return response


@app.errorhandler(404)
def page_not_found(error):
    """Custom 404 page."""
    return render_template('404.html'), 404


if __name__ == '__main__':
    app.run(debug=True,host="0.0.0.0",port="8888")
