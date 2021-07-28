from dbcuts import dbshorts
import traceback
from flask import request, Response
import json
import secrets

# Login
def login():
    try:
        username = request.json["username"]
        password = request.json["password"]
    except:
        traceback.print_exc()
        print("Welp, something went wrong")
        return Response("User Data Error", mimetype="text/plain", status=400)

    hash_pass = dbshorts.get_hash_pass(username, password)
    rows_inserted = None
    try:
        user = dbshorts.run_selection("select id from users u where u.username=? and u.password=?", 
                                      [username, hash_pass])
        if(len(user) == 1):
            token = secrets.token_urlsafe(55)
            rows_inserted = dbshorts.run_insertion("insert into user_session (login_token, user_id) values (?,?)", 
                                                   [token, user[0][0]])
    except: 
        traceback.print_exc()
        print("Oh no, something went wrong")

    if(rows_inserted != None):
        login_dictionary = { "login_token": token }
        login_json = json.dumps(login_dictionary, default=str)
        return Response(login_json, mimetype="application/json", status=201)
    else:
        return Response("Invalid Login, Please Try Again", mimetype="text/plain", status=400)

# Logout
def logout():
    try:
        login_token = str(request.json['loginToken'])
    except KeyError:
        return Response("Bruh, where the tooken at?", mimetype="text/plain", status=422)
    except:
        traceback.print_exc()
        print("something went wrong, unknown error")

    rows = dbshorts.run_deletion("delete from user_session where login_token = ?", 
                                 [login_token,])
    if(rows == 1):
        return Response("Logout Successful", mimetype="text/plain", status=200)
    else:
        return Response("DB Error", mimetype="text/plain", status=500)

