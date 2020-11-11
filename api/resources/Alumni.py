from flask_restful import Resource
from api.resources import load_json, validate_admin_token, load_header_token
from api.models import db, object_as_dict
from api.models.alumni import *
from datetime import datetime as dt
from sqlalchemy import extract


class AlumniAdditionResource(Resource):
    def post(self):

        data = load_json()

        token = load_header_token()

        message, error_code = validate_admin_token(token)

        if message:
            return message, error_code

        # get the data
        try:
            first_name = data['first_name']
            last_name = data['last_name']

        except KeyError:
            return {'message': f"must include first_name and last_name"}, 400

        # check if the alumni exists
        test_alumni = AlumniModel.query.filter_by(
            first_name=first_name).filter_by(last_name=last_name).first()

        if test_alumni:
            return {'message': f"There is already an account associated with {last_name}, {first_name}."}, 403

        new_alumni = AlumniModel(first_name=first_name, last_name=last_name)

        try:
            linkedin_url = data['linkedin_url']
            new_alumni.linkedin_url = linkedin_url
        except KeyError:
            linkedin_url = ""

        try:
            job_title = data['job_title']
            new_alumni.job_title = job_title
        except KeyError:
            job_title = ""

        try:
            job_title_role = data['job_title_role']
            new_alumni.job_title_role = job_title_role
        except KeyError:
            job_title_role = ""

        try:
            job_company = data['job_company']
            new_alumni.job_company = job_company
        except KeyError:
            job_company = ""

        try:
            job_company_industry = data['job_company_industry']
            new_alumni.job_company_industry = job_company_industry
        except KeyError:
            job_company_industry = ""

        try:
            job_company_locations_locality = data['job_company_locations_locality']
            new_alumni.job_company_locations_locality = job_company_locations_locality
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

        '''
        new_alumni = AlumniModel(first_name=first_name, last_name=last_name, linkedin_url=linkedin_url,
                                 job_title=job_title, job_title_role=job_title_role, job_company_industry=job_company_industry,
                                 job_company_locations_locality=job_company_locations_locality)
        '''

        for number in phone_numbers:
            new_alumni.phone_numbers.append(PhoneNumberModel(
                ph_number=number, alumni_id=new_alumni.id))

        for email in emails:
            new_alumni.emails.append(EmailModel(
                email=email, alumni_id=new_alumni.id))

        for interest in interests:
            new_alumni.interests.append(InterestModel(
                interest=interest, alumni_id=new_alumni.id))

        for experience in experiences:

            try:

                new_experience = ExperienceModel(start_date=dt.strptime(experience['start_date'], "%Y-%m-%d"),
                                                 end_date=dt.strptime(experience['end_date'], "%Y-%m-%d"), title_name=experience[
                                                     'title_name'], title_role=experience['title_role'],
                                                 alumni_id=new_alumni.id)

                new_location = LocationModel(city=experience['company']['location']['city'], state=experience['company']['location']['state'],
                                             country=experience['company']['location'][
                                                 'country'], zipcode=experience['company']['location']['zipcode'],
                                             locality=experience['company']['location']['locality'])

                new_company = CompanyModel(
                    name=experience['company']['name'], experience_id=new_experience.id)

                new_location.company_id = new_company.id
                new_company.location = [new_location]
                new_experience.company = [new_company]

                new_alumni.experiences.append(new_experience)

            except KeyError:
                return {'message': f"key error with experiences"}, 500

            except:
                return {'message': f"error adding experience"}, 500

        for school in education:

            try:
                new_school = SchoolModel(name=school['name'], start_date=dt.strptime(school['start_date'], "%Y-%m-%d"),
                                         end_date=dt.strptime(school['end_date'], "%Y-%m-%d"), alumni_id=new_alumni.id)

                for major in school['majors']:
                    new_major = MajorModel(
                        name=major['name'], school_id=new_school.id)
                    new_school.majors.append(new_major)

                for minor in school['minors']:
                    new_minor = MinorModel(
                        name=minor['name'], school_id=new_school.id)
                    new_school.minors.append(new_minor)

                new_alumni.education.append(new_school)

            except:
                return {'message': f"error adding education"}, 500

        db.session.add(new_alumni)
        db.session.commit()

        return {'status': 'success', 'message': f"Added {new_alumni.first_name}, {new_alumni.last_name}"}, 201

    def delete(self):
        data = load_json()

        # validate the admin
        token = load_header_token()

        message, error_code = validate_admin_token(token)

        if message:
            return message, error_code

        # find the user to delete via email
        alumni_id = data['alumni_id']
        alumni_first_name = data['first_name']
        alumni_last_name = data['last_name']
        alumni = AlumniModel.query.filter_by(id=alumni_id).first()

        # if no user, return so
        if not alumni:
            return {'message': f"no account associated with {alumni_id}, {alumni_first_name}, {alumni_last_name}"}, 406

        # else delete the user
        db.session.delete(alumni)
        db.session.commit()

        return {'status': 'success', 'message': f"Deleted {alumni_id}, {alumni_first_name}, {alumni_last_name}"}, 204


class AlumniAccessResource(Resource):
    def get(self):

        # get the data
        try:
            alumni = [object_as_dict(person)
                      for person in AlumniModel.query.all()]

            return {'alumni': alumni}, 200

        except:
            return {'message': f"error returning alumni"}, 500


class AlumniFilterResource(Resource):
    def get(self):

        # get the data based on a filter
        data = load_json()

        # dict of filter parameters
        # ex. 'first_name' : "first name filter" etc
        '''
        filters: last name, graduation year, company, job title, industry

        '''

        filter_params = {}

        try:
            filter_params = data['filter']
        except:
            return {'message': f"filter not defined properly"}, 400

        results = []

        try:
            if (filter_params['grad_year'] != ""):

                results = db.session.query(AlumniModel).join(SchoolModel).filter(AlumniModel.last_name.like(filter_params['last_name'] + "%"),
                                                                                 AlumniModel.job_company.like(
                                                                                     filter_params['job_company'] + "%"),
                                                                                 AlumniModel.job_title.like(
                                                                                     filter_params['job_title'] + "%"),
                                                                                 AlumniModel.job_company_industry.like(
                    filter_params['job_company_industry'] + "%"),
                    SchoolModel.name.like("Georgetown%"), extract('year', SchoolModel.end_date) == dt.strptime(filter_params['grad_year'], "%Y").year).all()

            else:
                results = AlumniModel.query.filter(AlumniModel.last_name.like(filter_params['last_name'] + "%"),
                                                   AlumniModel.job_company.like(
                                                       filter_params['job_company'] + "%"),
                                                   AlumniModel.job_title.like(
                                                       filter_params['job_title'] + "%"),
                                                   AlumniModel.job_company_industry.like(filter_params['job_company_industry'] + "%")).all()
        except:
            return {'message': f"error with filters"}, 500

        try:
            alumni = [object_as_dict(person)
                      for person in results]

            return {'alumni': alumni}, 200

        except:
            return {'message': f"error returning alumni"}, 500


class AlumniFilterOptionsResource(Resource):
    def get(self):

        # should return a list of possible choices for a filter
        data = load_json()

        filter_type = data['filter_type']

        unique_options = []

        try:
            if (filter_type == "job_company"):

                unique_options = [item.job_company for item in db.session.query(
                    AlumniModel.job_company).distinct()]

            elif (filter_type == "job_title"):

                unique_options = [item.job_title for item in db.session.query(
                    AlumniModel.job_title).distinct()]

            elif (filter_type == "job_company_industry"):

                unique_options = [item.job_company_industry for item in db.session.query(
                    AlumniModel.job_company_industry).distinct()]

            elif (filter_type == "last_name"):

                unique_options = [item.last_name for item in db.session.query(
                    AlumniModel.last_name).distinct()]

            elif (filter_type == "grad_year"):

                # not sure if this works yet
                schools = db.session.query(SchoolModel).filter(SchoolModel.name.like("Georgetown%"),
                                                               extract('year', SchoolModel.end_date) != dt.strptime("1000", "%Y").year).all()

                unique_options = [item.end_date.year for item in schools]

                options_set = set(unique_options)

                unique_options = list(options_set)

            else:
                return {'message': f"invalid filter type"}, 400

        except:
            return {'message': f"error returning filter options"}, 500

        return {'options': unique_options}, 200
