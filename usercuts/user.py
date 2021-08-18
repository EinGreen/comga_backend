from dbcuts import dbshorts
import traceback
from flask import request, Response
import json

# creating new user
def create_user():
    try:
        username = request.json["username"]
        user_email = request.json["email"]
        user_pass = request.json["password"]
        is_author = bool(request.json.get("is_author"))
        salt = dbshorts.create_salt()
    except KeyError:
        return Response("Please enter required data", mimetype='text/plain', status=401)
    except:
        traceback.print_exc()
        print("Yeah, something went wrong with collecting the json data in create_user")
        return Response("Data Error, request invalid", mimetype="text/plain", status=400)
    hash_pass = dbshorts.create_hash_pass(salt, user_pass)

    if(is_author != None or is_author != '' or is_author == False):
        newuser_id = dbshorts.run_insertion("insert into users (username, email, password, salt) values (?,?,?,?)", 
                                            [username, user_email, hash_pass, salt])
    else:
        newuser_id = dbshorts.run_insertion("insert into users (username, email, password, is_author, salt) values (?,?,?,?,?)", 
                                            [username, user_email, hash_pass, is_author, salt])
    if(newuser_id == None):
        return Response("Database Error", mimetype="text/plain", status=500)
    else:
        newuser = [username, user_email, user_pass]
        newuser_json = json.dumps(newuser, default=str)
        print(f"{username} was successfully created!")
        return Response(newuser_json, mimetype="application/json", status=201)

# see user info
def get_user():
    try:
        user_id = request.json["userId"]
    except ValueError:
        return Response("Invalid user ID", mimetype='text/plain', status=422)
    except IndexError:
        return Response("User not found", mimetype="text/plain", status=404)
    except:
        traceback.print_exc()
        print("Cannot find user info")
        return Response("Data Error", mimetype="text/plain", status=400)

    user_info = dbshorts.run_selection("select u.id, username, email, image_url, from users u inner join user_session us on u.id = us.user_id where us.user_id=?", 
                                        [user_id])
    if(user_info == None):
        return Response("User not logged in", mimetype="text/plain", status=500)
    elif(len(user_info) == 0):
        return Response("User does not exsist", mimetype="text/plain", status=404)
    else:
        logged_in_dictionary = {
            "userId": user_info[0][0], "username": user_info[0][1], "email": user_info[0][2], "imageUrl": user_info[0][3]}
        log_json = json.dumps(logged_in_dictionary, default=str)
        return Response(log_json, mimetype="application/json", status=201)

# remove user
def delete_user():
    try:
        token = str(request.json['loginToken'])
        password = request.json['password']
    except:
        traceback.print_exc()
        print("You tried, but failed")

    username = dbshorts.run_selection("select u.username from users u inner join user_session us on u.id = us.user_id where us.login_token = ?", 
                                      [token])
    hash_pass = dbshorts.get_hash_pass(username[0][0], password)
    user_info = dbshorts.run_selection("select u.id, u.username from users u inner join user_session us on u.id = us.user_id where us.login_token = ? and u.password = ?", 
                                       [token, hash_pass,])
    if(user_info != None):
        rows = dbshorts.run_deletion("delete from users where id = ?", [user_info[0][0],])
        if(rows == 1):
            return Response(f"{user_info[0][1]} has been deleted", mimetype="text/plain", status=200)
        else:
            return Response("DB Error", mimetype="text/plain", status=500)
    else:
        return Response("Could not fine user", mimetype="text/plain", status=404)
    
