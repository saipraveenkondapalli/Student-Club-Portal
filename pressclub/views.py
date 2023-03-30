from flask import render_template, url_for, redirect, request, abort, session, flash
from flask_login import login_required, current_user, login_user, logout_user
from itsdangerous import Serializer, BadSignature, SignatureExpired

from pressclub import app, bcrypt
from pressclub.mails import send_mail
from pressclub.models import Users, Events


@app.route('/')
def index():
    admin = Users.objects(role=0).first()

    return render_template('index.html', name = admin)


@app.route('/login', methods = ['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('username')
        password = request.form.get('password')
        user = Users.objects(email=email).first()
        if user and bcrypt.check_password_hash(user.password, password):
            login_user(user)
            session['user_id'] = str(user.id)

            return redirect(url_for('index'))
    if current_user.is_authenticated:
        return redirect('/dashboard')

    return render_template('login.html')


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('index'))


@app.route('/forget', methods = ['GET', 'POST'])
def forget():
    if request.method == 'POST':
        email = request.form.get('username')
        user = Users.objects(email=email).first()
        if user:
            send_mail(email)
            return 'Mail sent'
        else:
            return f'User with email {email} does not exist'

    return render_template('forget.html')


@app.route('/reset/<token>', methods = ['GET', 'POST'])
def reset(token):
    s = Serializer(app.config['SECRET_KEY'])  # creates a serializer object
    try:
        email = s.loads(token, salt= 'reset',  max_age=600)  # max age is 10 minutes   i.e 600 seconds
        user = Users.objects(email=email).first()
        print(str(user.id))
        if request.method == 'POST':
            password_hash = bcrypt.generate_password_hash(request.form['password']).decode('utf-8')
            user.password = password_hash
            user.save()
            return redirect('/login')

    except SignatureExpired:  # if the token is expired
        return render_template("forget.html", msg="The token is expired")

    except BadSignature:  # if the token is invalid
        return render_template("forget.html", msg="The token is invalid")

    return render_template('reset.html', username=user.name)


@app.route('/register/<token>', methods = ['GET', 'POST'])
def register(token):
    s = Serializer(app.config['SECRET_KEY'])
    try:
        email = s.loads(token,salt='register', max_age=604800 ) # max age is 7 days in seconds = 604800
    except SignatureExpired:
        return '<h1>The token is expired</h1>'
    except BadSignature:
        return '<h1>The token is invalid</h1>'

    if request.method == "POST":
        roll_no  = request.form.get('roll_no').lower()
        name = request.form.get('name')
        department = request.form.get('department')
        batch = request.form.get('batch')
        phone = request.form.get('phone')
        password = request.form.get('password')
        password = bcrypt.generate_password_hash(password).decode('utf-8')
        email = email.lower()
        user = Users(email=email, roll_no=roll_no, name=name, department=department, batch=batch, phone=phone, password=password, role=2)
        user.save()
        flash('Account created successfully', 'success')
        return redirect('/login')

    return render_template('admin/register.html', email=email)


@app.route('/dashboard')
@login_required
def dashboard():
    events = Events.objects().order_by('-meeting_id')
    if current_user.role == 0:
        return render_template('admin/dashboard.html', events=events)
    elif current_user.role == 1:
        return render_template('coordinator/dashboard.html', events=events)
    elif current_user.role == 2:
        return render_template('student/dashboard.html', events=events)
    else:
        return abort(403)
