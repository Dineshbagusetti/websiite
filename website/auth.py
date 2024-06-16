from flask import Blueprint,render_template, request, flash, redirect, url_for
from .models import User
from werkzeug.security import generate_password_hash, check_password_hash
from . import db
from flask_login import login_user,login_required,logout_user,current_user

auth=Blueprint('auth',__name__)
@auth.route('/login', methods=['GET','POST'])
def login():
    if request.method == 'POST':
        email=request.form.get('email')
        password=request.form.get('password')
        user=User.query.filter_by(email=email).first()
        if user:
            if check_password_hash(user.password,password):
                flash('logged in successfully', category='success')
                login_user(user,remember=True)
                return redirect(url_for('views.home'))
            else:
                flash('incorrect password,tryagain', category='error')
        else:
            flash('incorrect user', category='error') 
    return render_template("login.html", user= current_user)

@auth.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('auth.login'))

@auth.route('/signup', methods=['GET','POST'])
def signup():
    if request.method=='POST':   
        email=request.form.get('email')
        first_name=request.form.get('firstName')
        password1=request.form.get('password1')
        password2=request.form.get('password2')
        
        
        user=User.query.filter_by(email=email).first()
        if user:
            flash('email already exist', category='error')
        elif len(email)<4:
            flash("email is must be greater than 4 characters ", category="error")
        elif len(first_name)<2:
            flash("firstname is must be greater than 2 characters ", category="error")
        elif len(password1)<7:
            flash("password1 is must be greater than 7 characters ", category="error")
        elif password1!=password2:
            flash("password1 is not equal to password2 ", category="error")
        else:
            new_user=User(email=email,first_name=first_name,password=generate_password_hash(password1,method='sha256'))
            db.session.add(new_user)
            db.session.commit()
            login_user(new_user,remember=True)
            flash("account created", category="success")
            return redirect(url_for('views.home'))
    return render_template("signup.html", user=current_user)
