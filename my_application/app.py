from flask import render_template, session, redirect, request, flash, url_for
from datetime import datetime
from models import Users,users_schema, credential_schema,schma_update_user_information, question_schema, answer_schema

import users
import build_database
import config
from config import db
import uuid
import json

app = config.connex_app


@app.route("/")
def home():
    return render_template("home.html") 

@app.route("/QNA", methods= ["POST", "GET"])
def QnA(): 
     #if "user" in session:
          #user= session["user"]
          values= users.read_all()
          for value in values: 
                    question = value.question
                    print(question)
                    flash(f"print {question}")
          if request.method== "POST": 
               id = uuid.uuid1()
               user= "pippo"
               answer= request.form["answer"]
               data= answer_schema.dump(Users(id_answer= id, answer = answer, username = user))
               users.create_answer(data)
          
          return render_template("QnA.html")

     #else: 
          #return redirect(url_for("login"))

@app.route("/Ask_question", methods= ["POST", "GET"])
def Ask_question(): 
     if "user" in session: 
          user =  session ["user"]
          if request.method ==  "POST":
               id = uuid.uuid1()
               print(id) 
               question= request.form["question"]
               print(question)
               data = question_schema.dump(Users(id_question= id, question= question, username= user))
               print(data)
               users.create_question(data)
     else: 
          return redirect(url_for("login"))
     return render_template("Ask_question.html")

@app.route ("/register", methods = ["POST", "GET"])
def register(): 
     if request.method == "POST": 
          session.permanent = True
          id = uuid.uuid1()
          user= request.form["usr"]
          email= request.form["email"]
          password= request.form["pswd"]
          user_info= users_schema.dump(Users(
               id = id,
               username= user,
               email=email,
               password= password))
          users.create(user_info)
          session["user"] = user 
          flash("Register Succesful !")
          return redirect(url_for("user"))
     else: 
          if "user" in session: 
               flash("You have been Registrated")
               return redirect(url_for("user")) 
          return render_template("register.html")
     

@app.route("/login", methods=["POST", "GET"])
def login():
     if request.method == "POST": 
          session.permanent = True
          email =  request.form ["email"]
          paswd = request.form["pswd"]
          credential= credential_schema.dump(Users( 
               email= email, 
               password= paswd))
          user= users.read_one(credential)
          print(user)
          session["user"] = user
          flash("Login Succesful!")
          if user == "admin":
              return redirect(url_for("admin")) 
          else:
               return redirect(url_for("user"))
     else: 
          if "user" in session: 
               flash("Already Login!")
               return redirect(url_for("user"))    
          return render_template("login.html")


@app.route("/user", methods= ["POST", "GET"])
def user():
     email = None
     if "user" in session :
          user = session["user"]
          if request.method == "POST": 
               print (18)
               email= request.form["email"]
               print(email)
               password = request.form["password"]
               print (password)
               information= schma_update_user_information.dump(Users(username = user, email= email, password= password))
               users.update(information)
               flash(f"succesfully update information")
               session["email"] = email
          else: 
               if "email" in session: 
                    email = session["email"]

          return render_template("user.html")
     else:
          flash("You are not Logged !")
          return redirect(url_for("login"))

@app.route("/logout")
def logout():
     if "user" in session: 
          user = session["user"] 
          flash(f"You have been logged out, {user}" , "info" )
     session.pop("user", None)
     session.pop("email", None)
     return redirect (url_for("login"))

@app.route("/admin", methods = ["POST", "GET"])
def admin(): 
     if "user" in session:
          user = session["user"]
          values = users.read_all()
          len(values)
          for value in values: 
               usernames = value.username
               print(usernames)
               if usernames != "admin":
                    flash(f"user on db, {usernames}" , "info" )
          if request.method=="POST":
               user_to_delete= request.form["username"]
               print(user_to_delete)
               users.delete(user_to_delete)
               flash(f"{user_to_delete} is been banned")
          return render_template("admin.html", username= usernames)




if __name__== "__main__":
     build_database
     app.run(host="0.0.0.0", port=8000, debug=True)
