from pressclub.models import Users, Events
from datetime import datetime
from pressclub import bcrypt


user = Users()
user.name = 'test'
user.email = '19a31b0444@pragati.ac.in'
user.password = bcrypt.generate_password_hash('qazwsxedc').decode('utf-8')
user.role = 1
user.phone = '1234567890'
user.batch = 2019
user.department = 'CSE'
user.roll_no = '19a31b0444'
user.badge = 1
user.save()