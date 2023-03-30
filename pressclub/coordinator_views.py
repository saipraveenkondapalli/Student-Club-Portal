import datetime
from flask import render_template, request, redirect, url_for, make_response, jsonify
from flask_login import login_required
from pressclub import app, coordinator_permission
from pressclub.models import Users, Events


@app.route('/add_event', methods=['GET', 'POST'])
@login_required
def add_event():
    if request.method == 'POST':
        title = request.form['title']
        venue = request.form['venue']
        date = request.form['date']
        number = request.form['number']
        time = request.form['time']
        date = datetime.datetime(int(date[0:4]), int(date[5:7]), int(date[8:10]))
        if Events.objects(datetime=date):
            return make_response(jsonify({'message': 'An Event already exists on given date'}), 400)
        else:
            event = Events(title=title, datetime=date, venue=venue, meeting_id=number, time=time)
            event.save()
            return make_response(jsonify({'message': 'Event added successfully'}), 200)

    return render_template('coordinator/add_event.html')


@app.route('/edit_event/<int:id>', methods=['GET', 'POST'])
@coordinator_permission.require(http_exception=403)
@login_required
def edit_event(id):
    event = Events.objects(meeting_id=id).first()
    if not event:
        return make_response(jsonify({'message': 'Event does not exist'}), 400)
    if request.method == 'POST':
        title = request.form['title']
        venue = request.form['venue']
        date = request.form['date']
        number = request.form['number']
        date = datetime.datetime(int(date[0:4]), int(date[5:7]), int(date[8:10]))
        event.title = title
        event.venue = venue
        event.datetime = date
        event.meeting_id = number
        event.save()
        return make_response(jsonify({'message': 'Event updated successfully'}), 200)
    return render_template('coordinator/edit_event.html', event=event)


@app.route('/assign_report', methods=['GET', 'POST'])
@coordinator_permission.require(http_exception=403)
@login_required
def assign_report():
    if request.method == "POST":
        roll_no = request.form['username'].lower()
        meeting_id = request.form['meeting_no']
        event = Events.objects(meeting_id=meeting_id).first()
        student = Users.objects(roll_no=roll_no).first()
        if not event:
            return make_response(jsonify({'message': 'Event does not exist'}), 400)
        if not student:
            return make_response(jsonify({'message': 'Student does not exist'}), 400)
        event.author = student
        event.save()
        return make_response(jsonify({'message': f'Report assigned successfully{event.author.name}'}), 200)
    return render_template('coordinator/assign_report.html')


@app.route('/coordinator/team', methods=['GET', 'POST'])
@coordinator_permission.require(http_exception=403)
@login_required
def coordinator_team():
    dcount = Users.objects(badge=1).count()
    rcount = Users.objects(badge=2).count()
    if request.method == "POST":
        department = request.form['department']
        year = int(request.form['year'])
        if year == 0 and department == "0":
            students = Users.objects().filter(role__in=[1, 2])
        elif year == 0:
            students = Users.objects(department=department).filter(role__in=[1, 2])
        elif department == "0":
            students = Users.objects(batch=year).filter(role__in=[1, 2])
        else:
            students = Users.objects(batch=year, department=department).filter(role__in=[1, 2])
        return render_template('coordinator/student_list.html', students=students)
    return render_template('coordinator/team.html', dcount=dcount, rcount=rcount)


@app.route('/attendance/<int:id>', methods=['GET', 'POST'])
@coordinator_permission.require(http_exception=403)
@login_required
def attendance(id):
    event = Events.objects(meeting_id=id).first()
    students = Users.objects().filter(role__in=[1, 2])
    if not event:
        return make_response(jsonify({'message': 'Event does not exist'}), 400)
    if request.method == "POST":
        attendees = request.form.getlist('checkbox')
        students = Users.objects().filter(roll_no__in=attendees, role__in=[1, 2])
        print(list(students))
        event.attendance = students
        event.absents = Users.objects(roll_no__nin=attendees, role__in=[1, 2])
        event.save()
        return make_response(jsonify({'message': 'Attendance marked successfully'}), 200)
    return render_template('coordinator/attendance.html', event=event, students=students)


@app.route('/delete', methods=['GET', 'POST'])
@coordinator_permission.require(http_exception=403)
@login_required
def delete():
    if request.method == "POST":
        department = request.form['department']
        year = int(request.form['year'])
        return redirect(url_for('delete_students', department=department, year=year))
    return render_template('coordinator/delete.html')


@app.route('/delete/<department>/<int:year>', methods=['GET', 'POST'])
@coordinator_permission.require(http_exception=403)
@login_required
def delete_students(department, year):
    department = str(department)
    students = student_list(department, year)
    if request.method == "POST":
        for student in students:
            print(student.name)
            student.delete()

        return make_response(jsonify({'message': 'Students deleted successfully'}), 200)
    return render_template('coordinator/delete_team.html', students=students, department=department, year=year)


@login_required
def student_list(department, year):
    year = int(year)
    if year == 0 and department == "0":
        students = Users.objects().filter(role__in=[1, 2])
    elif year == 0:
        students = Users.objects(department=department).filter(role__in=[1, 2])
    elif department == "0":
        students = Users.objects(batch=year).filter(role__in=[1, 2])
    else:
        students = Users.objects(batch=year, department=department).filter(role__in=[1, 2])

    return students


@app.route('/delete_event/<id>', methods=['GET', 'POST'])
@coordinator_permission.require(http_exception=403)
@login_required
def delete_event(id):
    event = Events.objects(meeting_id=id).first()
    if not event:
        return make_response(jsonify({'message': 'Event does not exist'}), 400)
    event.delete()
    return make_response(jsonify({'message': 'Event deleted successfully'}), 200)
