from werkzeug.wrappers import response
from dbcuts import dbshorts
import traceback
from flask import request, Response
import json
from usercuts import checks

def show_content():
    try:
        comic_info = dbshorts.run_selection("select c.id, c.read_type, c.title, c.author, c.cover, c.artist, c.status, c.tags, c.date_posted from content c;", [])
    except:
        traceback.print_exc()
        print("Sorry, can't get content")
        return Response("Could not get content", mimetype="text/plain", status=400)

    if(comic_info == None):
        return Response("Comic does not exsist", mimetype="text/plain", status=500)
    elif(len(comic_info) == 0):
        return Response("There are no Comics", mimetype="text/plain", status=404)
    else:
        print(comic_info)
        for comga in comic_info:
            comga_dictionary = {"comgaId": comga[0],
                                "type": comga[1],
                                "title": comga[2],
                                "author": comga[3],
                                "cover": comga[4],
                                "artist": comga[5]}
        comga_json = json.dumps(comga_dictionary, default=str)
        return Response(comga_json, mimetype="application/json", status=201)

def create_content():
    try: 
        token = str(request.json["loginToken"]) #* Required
        user_id = request.json["posterId"] #* Required
        read_type = str(request.json["readType"]) #* Required
        title = str(request.json["title"]) #* Required
        author = str(request.json["author"]) #* Required
        cover = str(request.json["cover"]) #* Required
        artist = str(request.json["artist"]) #* Required
        status = request.json.get("status")
        tags = request.json.get("tags")
    except IndexError:
        return Response("Data invalid", mimetype="text/plain", status=404)
    except KeyError:
        return Response("Dude, some of this stuff is required, you have to put it in the thing", mimetype="text/plain", status=406)
    except:
        traceback.print_exc()
        return Response("A thing went wrong", mimetype="text/plain", status=400)

    new_content = ""
    is_author = checks.check_author(token)

    if(is_author == None or "" or False):
        return Response("User not authorized to post content", mimetype="text/plain", status=401)
    elif(is_author != None and len(is_author) != 0):
        if((tags == None or "") and (status == None or "")):
            new_content = dbshorts.run_insertion("insert into content (read_type, title, author, cover, artist, poster_id) values (?,?,?,?,?,?)",
                                                 [read_type, title, author, cover, artist, user_id])
        elif(status == None or status == ""):
            new_content = dbshorts.run_insertion("insert into content (read_type, title, author, cover, artist, tags, poster_id) values (?,?,?,?,?,?,?)",
                                                 [read_type, title, author, cover, artist, tags, user_id])
        elif(tags == None or tags == ""):
            new_content = dbshorts.run_insertion("insert into content (read_type, title, author, cover, artist, status, poster_id) values (?,?,?,?,?,?,?)",
                                                 [read_type, title, author, cover, artist, status, user_id])
        else:
            new_content = dbshorts.run_insertion("insert into content (read_type, title, author, cover, artist, status, tags, poster_id) values (?,?,?,?,?,?,?,?)",
                                                 [read_type, title, author, cover, artist, status, tags, user_id])

        if(new_content != None or new_content != ""):
            content_info = dbshorts.run_selection("select c.id, c.read_type, c.title, c.author, c.cover, c.artist, c.status, c.tags, c.date_posted, c.poster_id from content c where c.id = ?", 
                                                  [new_content,])
            content_dictionary = {"contentId": content_info[0][0],
                                "readType": content_info[0][1],
                                "title": content_info[0][2],
                                "author": content_info[0][3],
                                "cover": content_info[0][4],
                                "artist": content_info[0][5],
                                "status": content_info[0][6],
                                "tags": content_info[0][7],
                                "datePosted": content_info[0][8],
                                "posterId": content_info[0][9]}
            content_json = json.dumps(content_dictionary, default=str)
            return Response(content_json, mimetype="application/json", status=201)
        else:
            return Response("Database Error, something went wrong on our end, sorry mate", mimetype="text/plain", status=500)
    else:
        return Response("Error on posting content", mimetype="text/plain", status=401)

def delete_content():
    try:
        token = str(request.json["loginToken"])
        content_id = request.json["contentId"]
    except:
        traceback.print_exc()
        print("You tried, but failed")

    is_author = checks.check_author(token)
    if(is_author != None):
        rows = dbshorts.run_deletion("delete from content where id = ?", [content_id,])
        if(rows == 1):
            return Response("Content deleted", mimetype="text/plain", status=200)
        else:
            return Response("DB Error, deletion may have failed", mimetype="text/plain", status=500)
    else:
        return Response("Unauthorized", mimetype="text/plain", status=401)

#! Under Testing    
def add_tag():
    try:
        token = str(request.json["loginToken"])
        content_id = request.json["contentId"]
        tags = request.json["tags"]
    except ValueError:
        return Response("Invalid content ID, stupid", mimetype="text/plain", status=422)
    except KeyError:
        return Response("Maditory Stuff, needs the input dude", mimetype="text/plain", status=401)
    except:
        traceback.print_exc()
        return Response("A thing went wrong", mimetype="text/plain", status=400)

    user_id = checks.check_session(token)
    tag_check = checks.tag_check(content_id)

    print(tag_check)

    if(user_id != None and content_id != None):
        user_id = int(user_id[0][0])
        if(tag_check != None or ""):
            tags = tag_check[0][0] + tags
        rows = dbshorts.run_update("from mvp_comga update content c set c.tags = ? where c.id = ?",
                                          [tags, content_id])
        if(rows != None or ""):
            updated_tags = tag_check
            return Response(updated_tags, mimetype="text/plain", status=200)
        else:
            return Response("Okay, for some reason you can't edit the tags. Bummer", mimetype='text/plain', status=500)
    elif(user_id == None or ""):
        return Response("User not found", mimetype="text/plain", status=404)
    elif(content_id == None or ""):
        return Response("Content not found", mimetype="text/plain", status=404)
