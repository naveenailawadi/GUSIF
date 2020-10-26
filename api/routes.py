from flask_restful import Api
from api import app
from api.resources.User import UserManagementResource, LoginResource
from api.resources.Admin import AdminUserManagementResource
from api.resources.Alumni import AlumniAdditionResource
from api.resources.Alumni import AlumniAccessResource

# create an api
api = Api(app)

# add user routes
api.add_resource(UserManagementResource, '/UserManagement')
api.add_resource(AdminUserManagementResource, '/AdminUserManagement')
api.add_resource(LoginResource, '/Login')

# alumni
api.add_resource(AlumniAdditionResource, '/AlumniAddition')
api.add_resource(AlumniAccessResource, '/AlumniAccess')
