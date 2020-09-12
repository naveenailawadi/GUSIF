from alumni import alumni_db
alumni_db.create_all()
 
from alumni import *


alan = AlumniModel(first_name = "Alan", last_name = "Balu")
bob = AlumniModel(first_name = "Bob", last_name = "Joe")

new_email1 = EmailModel(email = "alan12@georgetown.edu")
new_email2 = EmailModel(email = "bob12@georgetown.edu")

alan.emails.append(new_email1)
bob.emails.append(new_email2)

alumni_db.session.add(alan)
alumni_db.session.add(bob)
alumni_db.session.commit()


print(AlumniModel.query.all())

print(EmailModel.query.all())
