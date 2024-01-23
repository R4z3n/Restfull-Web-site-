from datetime import datetime
from config import app, db
from models import Users
import uuid

REQUEST_INFO= [{
    "id" : f"{uuid.uuid1()}",
    "username": "admin", 
    "email" : "admin@system.it", 
    "password":"duahndsoa",
    "id_answer" : f"{uuid.uuid1()}", 
    "answer": "print(1)", 
    "id_question": f"{uuid.uuid1()}",
    "question": "come si stampa un numero ?"

}]

with app.app_context():
    db.drop_all()
    db.create_all()
    for data in REQUEST_INFO:
        new_user = Users(id= data.get("id"),username=data.get("username"), email=data.get("email"), password= data.get("password"), id_answer= data.get("id_answer"),answer= data.get("answer"), id_question= data.get("id_question"), question= data.get("question"))
        db.session.add(new_user)
    db.session.commit()  

