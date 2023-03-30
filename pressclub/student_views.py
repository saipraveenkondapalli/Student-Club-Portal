from flask import render_template, request, jsonify, make_response
from flask_login import current_user, login_required
from pressclub import app, student_permission


@app.route('/student/profile', methods=['GET', 'POST'])
@student_permission.require(http_exception=403)
@login_required
def student_profile():
    if request.method == 'POST':
        mail = request.form['mail']
        phone = request.form['phone']
        if mail:
            current_user.email = mail
        if phone:
            current_user.phone = phone
        try:
            current_user.save()
        except:
            return make_response(jsonify({'message': 'Error in saving'}), 400)
        return make_response(jsonify({'message': 'Profile updated successfully'}), 200)
    return render_template('student/profile.html')

