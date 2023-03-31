from flask import render_template, abort, request, send_file
from flask_login import current_user, login_required

from pressclub import app
from pressclub.custom_functions import *
from pressclub.models import Events


@app.route('/reports', methods=['GET', 'POST'])
def reports():
    events = Events.objects.order_by('-meeting_id')
    json_data = []
    for event in events:
        meeting_id = event.meeting_id
        meeting_date = event.datetime.strftime('%d-%m-%Y')

        author = event.author.name
        title = event.title
        description = event.description
        json_data.append({'meeting_id': meeting_id, 'meeting_date': meeting_date, 'author': author, 'title': title, 'description': description})


    if current_user.is_authenticated:
        if current_user.role == 1:
            return render_template('coordinator/reports.html', events=json_data)
        elif current_user.role == 0:
            return render_template('admin/reports.html', events=json_data)
        elif current_user.role == 2:
            return render_template('student/reports.html', events=json_data)
    else:
        return render_template('reports.html', events=json_data)


@app.route('/view_report/<id>', methods=['GET', 'POST'])
def view_report(id):
    event = Events.objects(meeting_id=id).first()
    if event:
        if current_user.is_authenticated:
            if current_user.role == 1:
                return render_template('coordinator/view.html', event=event)
            if current_user.role == 0:
                return render_template('admin/view.html', event=event)
            elif current_user.role == 2:
                return render_template('student/view.html', event=event)
        else:
            return render_template('view.html', event=event)
    else:
        return """<script>alert("Invalid meeting id");window.location='/dashboard';</script>"""


@app.route('/write_report/<id>', methods=['GET', 'POST'])
@login_required
def write_report(id):
    event = Events.objects(meeting_id=id).first()
    if not event:
        return f"""<script>alert("Invalid meeting id");window.location='{request.url}';</script>"""
    # ------------------------------------ SAVE REPORT ------------------------------------ #
    if request.method == 'POST':
        report = str(request.form.get('report'))
        event.description = report
        # get the image from the form
        image = gdrive_image(request.form.get('image'))
        # save the image to event object
        event.image = image
        event.save()

    if event:
        if current_user.role == 1:
            return render_template('coordinator/write_report.html', event=event)
        elif current_user.role == 2:
            return render_template('student/write_report.html', event=event)


@app.route('/grammar_check/<text>', methods=['GET'])
def grammar_check(text):
    return grammar_check_api(text)


def gdrive_image(image_link):
    image_id = image_link.split('/')[-2]
    return str(f"https://drive.google.com/uc?export=view&id={image_id}")
