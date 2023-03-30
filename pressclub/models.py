import datetime
import random
import string
from datetime import datetime

from flask_login import UserMixin

from . import db, bcrypt, app, principals, session, Identity, RoleNeed, UserNeed


@app.login_manager.user_loader
def load_user(user_id):
    return Users.objects(pk=user_id).first()


@principals.identity_loader
def load_identity():
    user_id = session.get('user_id')
    if user_id:
        user = Users.objects(id=user_id).first()
        if user:
            identity = Identity(user_id)
            identity.user = user

            # Add the UserNeed to the identity
            identity.provides.add(UserNeed(user_id))

            # Add the role to the identity
            identity.provides.add(RoleNeed(str(user.role)))

            return identity
    return None


class Users(db.Document, UserMixin):
    roll_no = db.StringField(max_length=10, unique=True)
    email = db.EmailField(required=True, unique=True)
    password = db.StringField(required=True)
    name = db.StringField(required=True)
    role = db.IntField(required=True)
    badge = db.IntField()
    is_active = db.BooleanField(default=True)
    phone = db.StringField(required=True)
    batch = db.IntField()
    department = db.StringField()
    joining_date = db.StringField(default=datetime.today().strftime('%d-%m-%Y'))
    depature_date = db.StringField()

    meta = {
        'collection': 'users',
    }

    def __repr__(self):
        return f"User('{self.email}', '{self.name}')"

    @staticmethod
    def generate_password():
        password = ''.join(random.choice(string.ascii_letters + string.digits) for _ in range(8))
        password_hash = bcrypt.generate_password_hash(password).decode('utf-8')
        return password_hash

    @staticmethod
    def year(year):
        current_year = datetime.today().year
        month = datetime.today().month
        if month > 8:
            batch = current_year + 4 - year + 1
        else:
            batch = current_year + 4 - year
        return str(batch)


class Events(db.Document):
    meeting_id = db.IntField(required=True)
    title = db.StringField(required=True)
    datetime = db.DateTimeField(required=True)
    time = db.StringField(required=True)
    venue = db.StringField(required=True)
    description = db.StringField()
    author = db.ReferenceField(Users)
    image = db.StringField()
    report = db.StringField()
    attendance = db.ListField(db.ReferenceField(Users))
    absents = db.ListField(db.ReferenceField(Users))
    attendance_percentage = db.FloatField()

    meta = {
        'collection': 'events',
    }

    def __repr__(self):
        return f"Event('{self.title}', '{self.datetime}')"
