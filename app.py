from flask import Flask
import sys

app = Flask(__name__)

# The stuff
from usercuts import logins, user
# user
@app.get("/api/user")
def see_user_info():
    return user.get_user()
@app.post("/api/newuser")
def create_user():
    return user.create_user()
@app.delete("/api/user")
def delete_user():
    return user.delete_user()
# Login
@app.post("/api/login")
def login():
    return logins.login()
@app.delete("/api/logout")
def logout():
    return logins.logout()

# The Content
#! Content has bugs
from contentcuts import content
@app.get("/api/content")
def get_comics():
    return content.show_content()
@app.post("/api/content")
def post_comic():
    return content.create_content()
@app.delete("/api/content")
def delete_content():
    return content.delete_content()



# # Master Controls
# from mastercontrols import mastercontroler
# @app.delete("/api/mastercontrol")
# def kill_comic():
#     return mastercontroler.kill_comic()
# @app.delete("/api/mastercontrol")
# def terminate_user():
#     return mastercontroler.kill_user()



if(len(sys.argv) > 1):
    mode = sys.argv[1]
else:
    print("No mode argument, please pass a mode argument when invoking the file")
    exit()

if(mode == "production"):
    import bjoern
    bjoern.run(app, "0.0.0.0", 5069)
elif(mode == "testing"):
    from flask_cors import CORS
    CORS(app)
    app.run(debug=True)
else:
    print("Invalid mode, please select either 'production' or 'testing'")
    exit()