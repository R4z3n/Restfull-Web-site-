from datetime import datetime
from marshmallow_sqlalchemy import fields

from config import db, ma


class Users(db.Model):
    __tablename__ = "users"
    id = db.Column(db.String)
    username = db.Column(db.String(32),primary_key=True ,unique=True)
    email = db.Column(db.String(32), unique= True)
    password = db.Column(db.String(32))
    id_answer= db.Column(db.String)
    answer= db.Column (db.String(32))
    id_question= db.Column(db.String)
    question= db.Column(db.String(32))
        
class UsersSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Users
        load_instance = True
        sqla_session = db.session

users_schema= UsersSchema()
credential_schema = UsersSchema(only=("email", "password")) 
schma_update_user_information= UsersSchema(only=("username", "email", "password"))
question_schema = UsersSchema(only= ("username", "id_question", "question"))
answer_schema = UsersSchema(only= ("username","id_answer","answer"))
