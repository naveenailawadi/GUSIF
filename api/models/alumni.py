from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

app.config['SECRET_KEY'] = '45e2b67051014e2ba07df47f533c1f14'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///alumni.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

class AlumniModel(db.Model):

    __tablename__ = 'alumni'
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(100))
    last_name = db.Column(db.String(100))
    linkedin_url = db.Column(db.String(100))
    job_title = db.Column(db.String(100))
    job_title_role = db.Column(db.String(100))
    job_company_industry = db.Column(db.String(100))
    job_company_locations_locality = db.Column(db.String(100))
    phone_numbers = db.relationship("PhoneNumberModel", backref="alumni")
    emails = db.relationship("EmailModel", backref="alumni")
    interests = db.relationship("InterestModel", backref="alumni")
    experiences = db.relationship("ExperienceModel", backref="alumni")
    education = db.relationship("SchoolModel", backref="alumni")

    def __repr__(self):
        return '<Alumni %r>' % self.first_name


class PhoneNumberModel(db.Model):
    __tablename__ = "phone_number"
    id = db.Column(db.Integer, primary_key=True)
    ph_number = db.Column(db.String(12))
    alumni_id = db.Column(
        db.Integer, db.ForeignKey("alumni.id"))


class EmailModel(db.Model):
    __tablename__ = "email"
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(100))
    alumni_id = db.Column(
        db.Integer, db.ForeignKey("alumni.id"))


class InterestModel(db.Model):
    __tablename__ = "interest"
    id = db.Column(db.Integer, primary_key=True)
    interest = db.Column(db.String(100))
    alumni_id = db.Column(
        db.Integer, db.ForeignKey("alumni.id"))


class ExperienceModel(db.Model):
    __tablename__ = "experience"
    id = db.Column(db.Integer, primary_key=True)
    company = db.relationship("Company", backref="experience")
    start_date = db.Column(db.DateTime)
    end_date = db.Column(db.DateTime)
    title_name = db.Column(db.String(100))
    title_role = db.Column(db.String(100))

    alumni_id = db.Column(
        db.Integer, db.ForeignKey("alumni.id"))


class CompanyModel(db.Model):
    __tablename__ = "company"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    location = db.relationship("Location", backref="company")

    experience_id = db.Column(
        db.Integer, db.ForeignKey("experience.id"))


class LocationModel(db.Model):
    __tablename__ = "location"
    id = db.Column(db.Integer, primary_key=True)
    city = db.Column(db.String(100))
    state = db.Column(db.String(100))
    country = db.Column(db.String(100))
    zipcode = db.Column(db.Integer)
    locality = db.Column(db.String(100))

    company_id = db.Column(
        db.Integer, db.ForeignKey("company.id"))


class SchoolModel(db.Model):
    __tablename__ = "school"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    start_date = db.Column(db.DateTime)
    end_date = db.Column(db.DateTime)
    majors = db.relationship("Major", backref="school")
    minors = db.relationship("Minor", backref="school")

    alumni_id = db.Column(
        db.Integer, db.ForeignKey("alumni.id"))


class MajorModel(db.Model):
    __tablename__ = "major"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50))

    school_id = db.Column(
        db.Integer, db.ForeignKey("school.id"))


class MinorModel(db.Model):
    __tablename__ = "minor"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50))

    school_id = db.Column(
        db.Integer, db.ForeignKey("school.id"))
