from flask import render_template, flash, redirect, url_for, session, request, Flask, g
from flask_login import login_user, logout_user, current_user, login_required
from app import app, db, lm 
from forms import SignupForm, SigninForm 
from app import db
from models import User

@app.route('/')


# def login_required(f):
#     @wraps(f)
#     def wrap (*args,**):
#         if "logged In" in session:
#             return f(*,**)
#         else:
#             Flash('login first')
#     return wraps

@lm.user_loader
def load_user(id):
    return User.query.get(int(id))

@app.before_request
def before_request():
    g.user = current_user



@app.route('/index')
def index():
    user = g.user
    posts = [ # fake array of posts 
        {
            'author' : { 'nickname': 'jacob'},
            'body' : 'beauty day'
        },
        {
            'author' : {'nickname': 'caddy'},
            'body' : ' baasd '
        }
    ]
    return render_template('index.html', title='home', user=user, posts=posts)



@app.route('/signup', methods=['GET', 'POST'])
def signup():
    
    form = SignupForm(request.form)
   
    if request.method == 'POST' and form.validate():
        newuser = User(form.nickname.data, form.email.data, form.password.data)
        db.session.add(newuser)
        db.session.commit()

        session['remember_me'] = form.remember_me.data

        session['Logged In'] = True
        session['email'] = newuser.email


        flash('Thanks for registering')
        return redirect(url_for('profile'))

    return render_template('signup.html', form=form)


@app.route('/signin', methods=['GET', 'POST'])
def signin():
    if g.user is not None and g.user.is_authenticated:
        return redirect(url_for('index'))

    form = SigninForm(request.form)
   
    if request.method == 'POST' and form.validate():
        user = User.query.filter_by(email = form.email.data).first()
        session['remember_me'] = form.remember_me.data
        session['email'] = form.email.data
        login_user(user)
        flash('Welcome Back')
        return redirect(url_for('profile'))
    
    # if 'remember_me' in session:
    #     remember_me = session['remember_me']
    #     session.pop('remember_me', None)
    # login_user(g.user, remember=remember_me)
    # return redirect(request.args.get('next') or url_for('profile'))

    return render_template('signin.html', form=form)



@app.route('/signout')
@login_required
def signout():
    if 'email' not in session:
        return redirect(url_for('signin'))
    logout_user()
    session.clear()
    #session.pop('email', None)
    return redirect(url_for('index'))



@app.route('/profile')
@login_required
def profile():
 
    if 'email' not in session:
        return redirect(url_for('signin'))

    user = User.query.filter_by(email = session['email']).first()

    if user is None:
        return redirect(url_for('signin'))
    else:
        return render_template('profile.html')