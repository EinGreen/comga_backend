import traceback
from flask import Flask
import sys

app = Flask(__name__)

# The stuff
from usercuts import logins, user
# user
@app.get("/api/user")
def see_user_info():
    user.get_user()
@app.post("/api/newuser")
def create_user():
    user.create_user()
@app.delete("/api/user")
def delete_user():
    user.delete_user()
# Login
@app.post("/api/login")
def login():
    logins.login()
@app.delete("/api/logout")
def logout():
    logins.logout()

from contentcuts import content
@app.get("/api/content")
def get_comics():
    content.show_content()

if(len(sys.argv) > 1):
    mode = sys.argv[1]
else:
    print("No mode argument, please pass a mode argument when invoking the file")
    exit()

if(mode == "production"):
    import bjoern
    bjoern.run(app, "0.0.0.0", 5021)
elif(mode == "testing"):
    from flask_cors import CORS
    CORS(app)
    app.run(debug=True)
else:
    print("Invalid mode, please select either 'production' or 'testing'")
    exit()