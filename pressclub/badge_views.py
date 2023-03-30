from flask import Flask, render_template, abort, request, jsonify, make_response, session
from flask_login import LoginManager, login_user, current_user, logout_user, login_required
from pressclub import app, db , bcrypt, principals, student_permission
from pressclub.models import Users, Events



@app.route('/distribute_badges', methods=['GET', 'POST'])
@login_required
def distribute():
    if request.method == "GET":
        if current_user.type == "coordinator":
            return render_template('coordinator/distribute_badges.html')
        elif current_user.type == "admin":
            return render_template('admin/distribute_badges.html')
    if request.method == "POST":
        roll_no = request.form['username'].lower()
        badge = request.form['badge']
        student = Users.objects(roll_no=roll_no).first()
        if not student:
            return make_response(jsonify({'message': 'Student does not exist'}), 400)
        student.badge = 1
        student.save()
        return make_response(jsonify({'message': 'Badge distributed successfully'}), 200)


@app.route('/badge_distributed_list', methods=['GET', 'POST'])
@login_required
def badge_distributed_list():
    State = "Distributed"
    if request.method == "GET":
        students = Users.objects(badge = 1).all()
        if current_user.type == "coordinator":
            return render_template('coordinator/badge_distributed_list.html',students = students, state=State)
        elif current_user.type == "admin":
            return render_template('admin/badge_distributed_list.html',students= students, state=State)


@app.route('/return_badges', methods=['GET', 'POST'])
@login_required
def return_badges():
    if request.method == "GET":
        if current_user.role == 1:
            return render_template('coordinator/return_badges.html')
        elif current_user.role == 0:
            return render_template('admin/return_badges.html')
    if request.method == "POST":
        roll_no = request.form['username'].lower()
        badge = request.form['badge']
        student = Users.objects(roll_no=roll_no).first()
        if not student:
            return make_response(jsonify({'message': 'Student does not exist'}), 400)
        student.badge = 2
        student.save()
        return make_response(jsonify({'message': 'Badge returned successfully'}), 200)


@app.route('/badge_returned_list', methods=['GET', 'POST'])
@login_required
def badge_returned_list():
    State = "Returned"
    if request.method == "GET":
        students = Users.objects(badge = 2).all()
        if current_user.role == 1:
            return render_template('coordinator/badge_returned_list.html',students = students, state=State)
        elif current_user.role == 0:
            return render_template('admin/badge_returned_list.html',students= students, state=State)

    return abort(403)

