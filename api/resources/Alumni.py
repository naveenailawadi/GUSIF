from flask_restful import Resource
from api.resources import load_json, validate_admin_token, load_header_token, TOKEN_MINUTES
from api.models import db, UserModel, validate_admin
from api.models.alumni import *


class AlumniAdditionResource(Resource):
    def post(self):

        data = load_json()

        message, error_code = validate_admin_token(data['token'])

        if message:
            return message, error_code

        #get the data
        try:
	        first_name = data['first_name']
		    last_name = data['last_name']
		
		except KeyError:
			return {'message': f"must include first_name and last_name"}, 404


		# check if the alumni exists
        test_alumni = AlumniModel.query.filter_by(first_name=first_name).first()

        if test_alumni:
            return {'message': f"There is already an account associated with {last_name}, {first_name}."}, 403

		try:
		    linkedin_url =  data['linkedin_url']
		except KeyError:
			linkedin_url = ""

		try:
		    job_title =  data['job_title']
	    except KeyError:
	    	job_title = ""

		try:
		    job_title_role = data['job_title_role']
	    except KeyError:
	    	job_title_role = ""

	    try:
		    job_company_industry = data['job_company_industry']
	    except KeyError:
	    	job_company_industry = ""

	    try:
		    job_company_locations_locality = data['job_company_locations_locality']
	    except KeyError:
	    	job_company_locations_locality = ""

        try:
            phone_numbers = data['phone_numbers']
        except KeyError:
            phone_numbers = []

        try:
            emails = data['emails']
        except KeyError:
            emails = []

        try:
            interests = data['interests']
        except KeyError:
            interests = []

        try:
            experiences = data['experiences']
        except KeyError:
            experiences = []

        try:
            education = data['education']
        except KeyError:
            education = []

        new_alumni = AlumniModel(first_name = first_name, last_name = last_name, linkedin_url = linkedin_url, 
        	job_title = job_title, job_title_role = job_title_role, job_company_industry = job_company_industry, 
        	job_company_locations_locality = job_company_locations_locality)

        for number in phone_numbers:
        	new_alumni.phone_numbers.append(PhoneNumberModel(ph_number = number, alumni_id = new_alumni.id))

        for email in emails
        	new_alumni.emails.append(EmailModel(email = email, alumni_id = new_alumni.id))

        for interest in interests
        	new_alumni.interests.append(InterestModel(interest = interest, alumni_id = new_alumni.id))

        for experience in experiences

        	try:

	        	new_experience = ExperienceModel(start_date = experience['start_date'], 
	        		end_date = experience['end_date'], title_name = experience['title_name'], title_role = experience['title_role'],
	        		alumni_id = new_alumni.id)

	        	new_location = LocationModel(city = experience['company']['location']['city'], state = experience['company']['location']['state'],
	        		country = experience['company']['location']['country'], zipcode = experience['company']['location']['zipcode'], 
	        		locality = experience['company']['location']['locality'])

	        	new_company = CompanyModel(name = experience['company']['name'], experience_id = new_experience.id)

	        	new_location.company_id = new_company.id
	        	new_company.location = new_location
	        	new_experience.company = new_company

	        	new_alumni.experiences.append(new_experience)

	        except:
	        	return {'message': f"error adding experience"}, 404

	    for school in education:

	    	try:
	    		new_school = SchoolModel(name = school['name'], start_date = school['start_date'], end_date = school['end_date'], 
	    			alumni_id = new_alumni.id)

	    		for major in school['majors']:
	    			new_major = MajorModel(name = major['name'], school_id = new_school.id)
	    			new_school.majors.append(new_major)

	    		for minor in school['minors']:
	    			new_minor = MinorModel(name = minor['name'], school_id = new_school.id)
	    			new_school.minors.append(new_minor)

	    		new_alumni.education.append(new_school)

	    	except:
	    		return {'message': f"error adding education"}, 404


	   	db.session.add(new_alumni)
		db.session.commit()

        return {'status': 'success', 'message': f"Added {new_alumni.first_name}, {new_alumni.last_name}"}, 201

    def delete(self):
        data = load_json()

        # validate the admin
        message, error_code = validate_admin_token(data['token'])
        if message:
            return message, error_code

        # find the user to delete via email
        alumni_id = data['alumni_id']
        alumni_first_name = data['first_name']
        alumni_last_name = data['last_name']
        alumni = AlumniModel.query.filter_by(id=alumni_id).first()

        # if no user, return so
        if not alumni:
            return {'message': f"no account associated with {alumni_id}, {alumni_first_name}, {alumni_last_name}"}, 404

        # else delete the user
        db.session.delete(alumni)
        db.session.commit()

        return {'status': 'success', 'message': f"Deleted {alumni_id}, {alumni_first_name}, {alumni_last_name}"}, 201


class AlumniAccessResource(Resource):
    def get(self):

    	data = load_json()

        message, error_code = validate_admin_token(data['token'])

        if message:
            return message, error_code

        #get the data
        try:
        	alumni = [{'first_name': person.first_name, 'last_name': person.last_name} for person in AlumniModel.query.all()]

       		return {'alumni': alumni}, 201

       	except:
       		return {'message': f"error returning alumni"}, 404
