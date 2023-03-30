from flask import render_template, request, make_response
from flask_login import login_required, current_user
from pressclub import app, admin_permission
from pressclub.mails import send_mail_to_create_user
from pressclub.models import Users


@app.route('/add_member', methods=['GET', 'POST'])
@admin_permission.require(http_exception=403)
@login_required
def add_member():
    if request.method == 'POST':
        email = request.form.get('email')
        user = Users.objects(email=email).first()
        if user:
            return 'User already exists'
        else:
            send_mail_to_create_user(email)
            make_response('Mail sent', 200)

    return render_template('admin/new_member.html')


@app.route('/admin_profile', methods=['GET', 'POST'])
@admin_permission.require(http_exception=403)
@login_required
def admin_profile():
    if request.method == 'POST':
        phone = request.form['phone']
        email = request.form['email']
        if phone:
            current_user.phone = phone
        if email:
            current_user.email = email
        current_user.save()
        return make_response('Profile updated', 200)

    return render_template('admin/profile.html')


@app.route('/assign_coordinator', methods=['GET', 'POST'])
@admin_permission.require(http_exception=403)
@login_required
def assign_coordinator():
    if request.method == 'POST':

        roll_no = request.form['roll_no'].lower()  # takes value from the html page with input name roll_no
        user = Users.objects(roll_no=roll_no).first()
        if user:
            user.role = 1
            user.save()
            return make_response('Coordinator assigned', 200)
        else:
            return make_response('User does not exist', 404)
    return render_template('admin/assign_coordinator.html')


@app.route('/revoke_coordinator', methods=['GET', 'POST'])
@admin_permission.require(http_exception=403)
@login_required
def revoke_coordinator():
    if request.method == 'POST':

        roll_no = request.form['roll_no'].lower()
        user = Users.objects(roll_no=roll_no).first()
        if user:
            user.role = 2
            user.save()
            return make_response('Coordinator revoked', 200)
        else:
            return make_response('User does not exist', 404)
    return render_template('admin/revoke_coordinator.html', coordinators=Users.objects(role=1))


@app.route('/team', methods=['GET', 'POST'])
@login_required
def team():
    if request.method == "POST":
        department = request.form['department']
        year = request.form['year']
        if year == '0' and department == '0':
            students = Users.objects(role__in=[1, 2])
        elif year == '0':
            students = Users.objects(department=department, role__in=[1, 2])
        elif department == '0':
            students = Users.objects(year=year, role__in=[1, 2])
        else:
            students = Users.objects(year=year, department=department, role__in=[1, 2])

        return render_template('admin/student_list.html', students=students)
    return render_template('admin/team.html')


@app.route('/edit_name/', methods=['GET', 'POST'])
@admin_permission.require(http_exception=403)
@login_required
def edit_name():
    if request.method == 'POST':
        name = request.form['name']
        current_user.name = name
        current_user.save()
        return make_response('Name updated', 200)
    return render_template('admin/edit_name.html')
