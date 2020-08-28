from sqlalchemy import Integer, ForeignKey, String, Column
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

from sqlalchemy import create_engine

Base = declarative_base()

class Alumni(Base):

	__tablename__ = 'alumni'
	ID = Column(Integer, primary_key = True)
	first_name = Column(String)
	last_name = Column(String)
	linkedin_url = Column(String)
	job_title = Column(String)
	job_title_role = Column(String)
	job_company_industry = Column(String)
	job_company_locations_locality = Column(String)
	phone_numbers = relationship("PhoneNumber", backref = "alumni")
	emails = relationship("Email", backref = "alumni")
	interests = relationship("Interest", backref = "alumni")
	experiences = relationship("Experience", backref = "alumni")
	education = relationship("School", backref = "alumni")

class PhoneNumber(Base):
	__tablename__ = "phone_number"
	ID = Column(Integer, primary_key = True)
	ph_number = Column(String(12))
	alumni_id = Column(Integer, ForeignKey("alumni.ID"))

class Email(Base):
	__tablename__ = "email"
	ID = Column(Integer, primary_key = True)
	address = Column(String(100))
	alumni_id = Column(Integer, ForeignKey("alumni.ID"))

class Interest(Base):
	__tablename__ = "interest"
	ID = Column(Integer, primary_key = True)
	interest = Column(String(100))
	alumni_id = Column(Integer, ForeignKey("alumni.ID"))

class Experience(Base):
	__tablename__ = "experience"
	ID = Column(Integer, primary_key = True)
	company = relationship("Company", backref = "experience")
	start_date = Column(String(20))
	end_date = Column(String(20))
	title_name = Column(String(100))
	title_role = Column(String(100))
	alumni_id = Column(Integer, ForeignKey("alumni.ID"))

class Company(Base):
	__tablename__ = "company"
	ID = Column(Integer, primary_key = True)
	name = Column(String(100))
	location = relationship("Location", backref = "Company")
	experience_id = Column(Integer, ForeignKey("experience.ID"))

class Location(Base):
	__tablename__ = "location"
	ID = Column(Integer, primary_key = True)
	city = Column(String(100))
	state = Column(String(100))
	country = Column(String(100))
	zipcode = Column(Integer)
	locality = Column(String(100))
	company_id = Column(Integer, ForeignKey("company.ID"))

class School(Base):
	__tablename__ = "school"
	ID = Column(Integer, primary_key = True)
	name = Column(String(100))
	start_date = Column(String(20))
	end_date = Column(String(20))
	majors = relationship("Major", backref = "School")
	minors = relationship("Minor", backref = "School")
	alumni_id = Column(Integer, ForeignKey("alumni.ID"))

class Major(Base):
	__tablename__ = "major"
	ID = Column(Integer, primary_key = True)
	name = Column(String(50))
	school_id = Column(Integer, ForeignKey("school.ID"))

class Minor(Base):
	__tablename__ = "minor"
	ID = Column(Integer, primary_key = True)
	name = Column(String(50))
	school_id = Column(Integer, ForeignKey("school.ID"))

engine = create_engine('sqlite:///AlumniDatabase.db')

Base.metadata.create_all(engine)

