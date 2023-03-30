import datetime
from flask import Flask, render_template, request, redirect, url_for, session
from flask_mongoengine import MongoEngine
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
from flask_bcrypt import Bcrypt
from flask_principal import Principal, Permission, RoleNeed, UserNeed, identity_loaded, Identity, AnonymousIdentity, identity_changed


app = Flask(__name__)

app.config['SECRET_KEY'] = 'sv;akn;kvnvknkvndk;kdksndkwnefajkndvnsdvksnv;dkvnskdnv;kdjvn;dvndv;n'
# --------------------------------------------FLASK Bcrypt CONFIGURATION -----------------------------------------------

bcrypt = Bcrypt(app)

# ----------------------------------------------------------------------------------------------------------------------

# ---------------------------------------- MongoDB ---------------------------------------------------------------------
app.config['MONGODB_SETTINGS'] = {
    'host': 'mongodb+srv://pressclub:pressclub2003@cluster0.0rjhtgo.mongodb.net/pressclub?retryWrites=true&w=majority'
}
db = MongoEngine(app)

# ----------------------------------------------------------------------------------------------------------------------



# ---------------------------------------- Login Manager ---------------------------------------------------------------

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

# ----------------------------------------------------------------------------------------------------------------------


#  ------------------------------------------------------------ User Roles ---------------------------------------------
principals = Principal(app)
admin_permission = Permission(RoleNeed('0'))
coordinator_permission = Permission(RoleNeed('1'))
student_permission = Permission(RoleNeed('2'))


# Limiting session to 24 hours
@app.before_request
def limit_session_to_24():
    session.permanent = True
    app.permanent_session_lifetime = datetime.timedelta(minutes=24)

