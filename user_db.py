from sqlalchemy import *

metadata = MetaData()

user = Table('user', metadata,
	Column('user_name', string(32), nullable = False), #REQUIRED
	Column('birthday',Date),
	Column('gender',string(1)),
	#Column('password',string(32), nullable = False), #REQUIRED
	Column('user_id',Integer, primary_key = True),
	Column('email_address', string(32), nullable = False) #REQUIRED
)