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
    return render_template("index.html") 

@app.route("/blog", methods= ["POST", "GET"])
def blog_post():
     return render_template("blog-post.html")

@app.route("/QNA", methods= ["POST", "GET"])
def QnA(): 
     if "user" in session:
          user= session["user"]
          values= users.read_all()
          for value in values: 
                    question = value.question
                    print(question)
                    answerdb= None
                    flash(f"print {question}")
          if request.method== "POST": 
               print(1)
               id = uuid.uuid1()
               user= "pippo"
               answer= request.form["answer"]
               answerdb= answer
               print(answer)
               data= answer_schema.dump(Users(id_answer= id, answer = answer, username = user))
               print(data)
               result = users.create_answer(data)
               print (result)
          
          return render_template("answer.html", question= question, user=user, answer=answerdb)

     else: 
          return redirect(url_for("login"))

@app.route("/Ask_question", methods= ["POST", "GET"])
def Ask_question(): 
     if "user" in session: 
          user =  session ["user"]
          if request.method ==  "POST":
               id = uuid.uuid1()
               print("sono dentro ask question")
               print(id) 
               question= request.form["question"]
               print(question)
               data = question_schema.dump(Users(id_question= id, question= question, username= user))
               print(data)
               users.create_question(data)
     else: 
          return redirect(url_for("login"))
     return render_template("question.html")

@app.route ("/register", methods = ["POST", "GET"])
def register(): 
     if request.method == "POST": 
          session.permanent = True
          id = uuid.uuid1()
          user= request.form["usr"]
          print(user)
          email= request.form["email"]
          print(email)
          password= request.form["pswd"]
          print(password)
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
          print(email)
          paswd = request.form["pswd"]
          print (paswd)
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
          values= users.read_all()
          for value in values:
               email= value.email
          flash(f"user")
          if request.method == "POST": 
               print (18)
               email= request.form["email"]
               print(f'email')
               password = request.form["password"]
               print (password)
               information= schma_update_user_information.dump(Users(username = user, email= email, password= password))
               users.update(information)
               flash(f"succesfully update information")
               session["email"] = email
          else: 
               if "email" in session: 
                    email = session["email"]

          return render_template("profile.html", user= user, email= email)
     else:
          flash("You are not Logged !")
          return redirect(url_for("login"))

@app.route("/edit_information", methods=["POST", "GET"])
def edit(): 
     email= None
     if "user" in session :
          user = session["user"]
          if request.method == "POST": 
               print (18)
               email= request.form["email"]
               print(f'email')
               password = request.form["password"]
               print (password)
               information= schma_update_user_information.dump(Users(username = user, email= email, password= password))
               users.update(information)
               flash(f"succesfully update information")
               session["email"] = email
          else: 
               if "email" in session: 
                    email = session["email"]

     return render_template("edit.html")

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
          usernames= None
          for value in values: 
               usernames = value.username
               quest = value.question
               ans = value.answer
               print(usernames)
               if usernames != "admin":
                    flash(f"user on db, {usernames}" , "info" )
          if request.method=="POST":
               user_to_delete= request.form["username"]
               print(user_to_delete)
               users.delete(user_to_delete)
               flash(f"{user_to_delete} is been banned")
          return render_template("admin.html", username= usernames, questions= quest, answare= ans)




if __name__== "__main__":
     build_database
     app.run(host="0.0.0.0", port=8000, debug=True)
