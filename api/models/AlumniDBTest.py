from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
 
from AlumniDB import *

engine = create_engine('sqlite:///AlumniDatabase.db')

Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)

session = DBSession()

new_alumni = Alumni(first_name = "Alan", last_name = "Balu")
session.add(new_alumni)
session.commit()

new_email1 = Email(address = "agb76@georgetown.edu1", alumni = new_alumni)
new_email2 = Email(address = "agb76@georgetown.edu2", alumni = new_alumni)

session.add(new_email1)
session.commit()

session.add(new_email2)
session.commit()