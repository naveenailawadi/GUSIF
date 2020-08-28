from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from datetime import datetime

app = Flask(__name__)

app.config['SECRET_KEY'] = '45e2b67051014e2ba07df47f533c1f14'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///alumni.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

alumni_db = SQLAlchemy(app)

class Alumni(alumni_db.Model):

	__tablename__ = 'alumni'
	id = alumni_db.Column(alumni_db.Integer, primary_key = True)
	first_name = alumni_db.Column(alumni_db.String(100))
	last_name = alumni_db.Column(alumni_db.String(100))
	linkedin_url = alumni_db.Column(alumni_db.String(100))
	job_title = alumni_db.Column(alumni_db.String(100))
	job_title_role = alumni_db.Column(alumni_db.String(100))
	job_company_industry = alumni_db.Column(alumni_db.String(100))
	job_company_locations_locality = alumni_db.Column(alumni_db.String(100))
	phone_numbers = alumni_db.relationship("PhoneNumber", backref = "alumni")
	emails = alumni_db.relationship("Email", backref = "alumni")
	interests = alumni_db.relationship("Interest", backref = "alumni")
	experiences = alumni_db.relationship("Experience", backref = "alumni")
	education = alumni_db.relationship("School", backref = "alumni")

	def __repr__(self):
		return '<Alumni %r>' % self.first_name

class PhoneNumber(alumni_db.Model):
	__tablename__ = "phone_number"
	id = alumni_db.Column(alumni_db.Integer, primary_key = True)
	ph_number = alumni_db.Column(alumni_db.String(12))
	alumni_id = alumni_db.Column(alumni_db.Integer, alumni_db.ForeignKey("alumni.id"))

class Email(alumni_db.Model):
	__tablename__ = "email"
	id = alumni_db.Column(alumni_db.Integer, primary_key = True)
	email = alumni_db.Column(alumni_db.String(100))
	alumni_id = alumni_db.Column(alumni_db.Integer, alumni_db.ForeignKey("alumni.id"))

class Interest(alumni_db.Model):
	__tablename__ = "interest"
	id = alumni_db.Column(alumni_db.Integer, primary_key = True)
	interest = alumni_db.Column(alumni_db.String(100))
	alumni_id = alumni_db.Column(alumni_db.Integer, alumni_db.ForeignKey("alumni.id"))

class Experience(alumni_db.Model):
	__tablename__ = "experience"
	id = alumni_db.Column(alumni_db.Integer, primary_key = True)
	company = alumni_db.relationship("Company", backref = "experience")
	start_date = alumni_db.Column(alumni_db.DateTime)
	end_date = alumni_db.Column(alumni_db.DateTime)
	title_name = alumni_db.Column(alumni_db.String(100))
	title_role = alumni_db.Column(alumni_db.String(100))

	alumni_id = alumni_db.Column(alumni_db.Integer, alumni_db.ForeignKey("alumni.id"))

class Company(alumni_db.Model):
	__tablename__ = "company"
	id = alumni_db.Column(alumni_db.Integer, primary_key = True)
	name = alumni_db.Column(alumni_db.String(100))
	location = alumni_db.relationship("Location", backref = "Company")

	experience_id = alumni_db.Column(alumni_db.Integer, alumni_db.ForeignKey("experience.id"))

class Location(alumni_db.Model):
	__tablename__ = "location"
	id = alumni_db.Column(alumni_db.Integer, primary_key = True)
	city = alumni_db.Column(alumni_db.String(100))
	state = alumni_db.Column(alumni_db.String(100))
	country = alumni_db.Column(alumni_db.String(100))
	zipcode = alumni_db.Column(alumni_db.Integer)
	locality = alumni_db.Column(alumni_db.String(100))

	company_id = alumni_db.Column(alumni_db.Integer, alumni_db.ForeignKey("company.id"))

class School(alumni_db.Model):
	__tablename__ = "school"
	id = alumni_db.Column(alumni_db.Integer, primary_key = True)
	name = alumni_db.Column(alumni_db.String(100))
	start_date = alumni_db.Column(alumni_db.DateTime)
	end_date = alumni_db.Column(alumni_db.DateTime)
	majors = alumni_db.relationship("Major", backref = "School")
	minors = alumni_db.relationship("Minor", backref = "School")

	alumni_id = alumni_db.Column(alumni_db.Integer, alumni_db.ForeignKey("alumni.id"))

class Major(alumni_db.Model):
	__tablename__ = "major"
	id = alumni_db.Column(alumni_db.Integer, primary_key = True)
	name = alumni_db.Column(alumni_db.String(50))

	school_id = alumni_db.Column(alumni_db.Integer, alumni_db.ForeignKey("school.id"))

class Minor(alumni_db.Model):
	__tablename__ = "minor"
	id = alumni_db.Column(alumni_db.Integer, primary_key = True)
	name = alumni_db.Column(alumni_db.String(50))

	school_id = alumni_db.Column(alumni_db.Integer, alumni_db.ForeignKey("school.id"))
