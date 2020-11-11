from api import db
from api import bcrypt
from api.secrets import ADMIN_PROFILE
from datetime import datetime as dt
from sqlalchemy.exc import NoInspectionAvailable


# create a user model
class UserModel(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(320), nullable=False, unique=True)
    password = db.Column(db.String(100), nullable=False)

    creation_date = db.Column(
        db.TIMESTAMP, server_default=db.func.current_timestamp())


# create a function to validate users
def validate_user(email, password):
    # get the user
    user = UserModel.query.filter_by(email=email).first()

    if not user:
        return False, {'message': f"no account associated with {email}"}, 404

    # check if passwords match
    if not bcrypt.check_password_hash(user.password, password):
        return False, {'message': f"incorrect password for {email}"}, 401

    return True, user, 201


def validate_admin(email, password):
    print(ADMIN_PROFILE['email'] + ' ' + ADMIN_PROFILE['password'])
    if email != ADMIN_PROFILE['email']:
        return False
    elif password != ADMIN_PROFILE['password']:
        return False
    else:
        return True

# check an attribute


def get_and_check_attribute(obj, c):
    try:
        value = getattr(obj, c.key)
    except NoInspectionAvailable:
        return None

    # check dt
    if type(value) is dt:
        value = value.strftime('%s')

    return value


def object_as_dict(obj):
    if obj:
        obj_dict = {c.key: get_and_check_attribute(obj, c)
                    for c in db.inspect(obj).mapper.column_attrs}
    else:
        obj_dict = {}
    return obj_dict


# make a function that copies models
def copy_model(model):
    db.session.expunge(model)

    db.make_transient(model)
    model.id = None

    # add the model back to the session and refresh the id
    db.session.add(model)
    db.session.flush()
    db.session.refresh(model)

    print(f"New id: {model.id}")

    return model
