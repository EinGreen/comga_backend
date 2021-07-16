from dbcuts import dbshorts
import traceback
from flask import Flask, request, Response
import json
import secrets
import sys

app = Flask(__name__)

# *User api
# creating new user
# TODO: try and make it so that it can get the image_url and/or the banner_url
@app.post("/api/newuser")
def create_user():
    try:
        username = request.json["username"]
        user_email = request.json["email"]
        user_pass = request.json["password"]
        user_bday = request.json["birthday"]
        user_bio = request.json["bio"]
        salt = dbshorts.create_salt()
    except:
        traceback.print_exc()
        print("Welp, something went wrong")
        return Response("Data Error, request invalid", mimetype="text/plain", status=400)
    hash_pass = dbshorts.create_hash_pass(salt, user_pass)

    newuser_id = dbshorts.run_insertion("insert into users (username, email, password, birthday, bio, salt) values (?,?,?,?,?,?)", 
                                        [username, user_email, hash_pass, user_bday, user_bio, salt])
    if(newuser_id == None):
        return Response("Database Error", mimetype="text/plain", status=500)
    else:
        newuser = [username, user_email, user_pass, user_bday, user_bio]
        newuser_json = json.dumps(newuser, default=str)
        print(f"{username} was successfully created!")
        return Response(newuser_json, mimetype="application/json", status=201)

# Get logged in users
@app.get("/api/user")
def get_user():
    try:
        user_id = request.json["userId"]
    except IndexError:
        return Response("User not found", mimetype="text/plain", status=404)
    except:
        traceback.print_exc()
        print("I have no idea what happened, but something went wrong")
        return Response("Data Error", mimetype="text/plain", status=400)

    user_info = dbshorts.run_selection("select u.id, username, email, bio, birthday, image_url, banner_url from users u inner join user_session us on u.id = us.user_id where us.user_id=?", 
                                        [user_id])
    if(user_info == None):
        return Response("User not logged in", mimetype="text/plain", status=500)
    elif(len(user_info) == 0):
        return Response("User does not exsist", mimetype="text/plain", status=404)
    else:
        logged_in_dictionary = {
            "userId": user_info[0][0], "username": user_info[0][1], "email": user_info[0][2], "bio": user_info[0][3], "birthdate": user_info[0][4], "imageUrl": user_info[0][5], "bannerUrl": user_info[0][6]}
        log_json = json.dumps(logged_in_dictionary, default=str)
        return Response(log_json, mimetype="application/json", status=201)

