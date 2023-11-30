from flask import abort, make_response
import json
from config import db
from models import Users,users_schema,schma_update_user_information

#interazioni con il DB 


def read_all():
    users = Users.query.all()
    print(len(users))
    return users

def read_one(credential):
    print(1)
    email= credential.get("email")
    password= credential.get("password")
    print (email)
    print(password)
    user = Users.query.filter(Users.email == email, Users.password == password).value(Users.username)
    print (user)

    if user is not None:
        return user
    else:
        abort(404, f"Person with last name {email} not found")

def create(user_info):
    username= user_info.get("username")
    print(username)
    existing_user = Users.query.filter(Users.username == username).one_or_none()
    if existing_user is None:
        print(1)
        print(user_info)
        new_user = users_schema.load(user_info,session=db.session)
        print(new_user)
        db.session.add(new_user)
        db.session.commit()
        return users_schema.dump(new_user), 201
    else:
        abort(406, f"Person with last name {username}already exists")

def update(update_information):
    username = update_information.get("username")
    print(username)
    existing_person = Users.query.filter(Users.username == username).one_or_none()

    if existing_person:
        information =users_schema.dump(Users(id = existing_person, username = username, email= update_information.get("email"),password = update_information.get("password")))
        update_user = users_schema.load(information, session=db.session)
        existing_person.email= update_user.email
        existing_person.password = update_user.password 
        db.session.merge(existing_person)
        db.session.commit()
        return users_schema.dump(existing_person), 201
    else:
        abort(404, f"Person with last name {username} not found")

def delete(username):
    existing_user = Users.query.filter(Users.username == username).one_or_none()

    if existing_user:
        db.session.delete(existing_user)
        db.session.commit()
        return make_response(f"{username} successfully deleted", 200)
    else:
        abort(404, f"Person with last name {username} not found")


def create_question(information): 
    id= information.get("id_question")
    print(id)
    existing_question = Users.query.filter(Users.id_question== id).one_or_none()
    if existing_question is None:
        print(1)
        print(information)
        new_user = users_schema.load(information,session=db.session)
        print(new_user)
        db.session.add(new_user)
        db.session.commit()
        return users_schema.dump(new_user), 201
    else:
        abort(406, f"Person with last name {id}already exists")

def create_answer(info):
    id= info.get("id_answer")
    print(id)
    existing_answer = Users.query.filter(Users.id_answer== id).one_or_none()
    if existing_answer is None:
        new_user = users_schema.load(info,session=db.session)
        print(new_user)
        db.session.add(new_user)
        db.session.commit()
        return users_schema.dump(new_user), 201
    else:
        abort(406, f"Person with last name {id}already exists")