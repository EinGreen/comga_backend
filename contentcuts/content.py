from dbcuts import dbshorts
import traceback
from flask import request, Response
import json
from usercuts import checks

def show_content():
    try:
        comic_info = dbshorts.run_selection("select c.id, c.type, c.title, c.author, c.cover, c.artist from content c", [])
    except:
        traceback.print_exc()
        print("Sorry, can't get content")
        return Response("Could not get content", mimetype="text/plain", status=400)

    if(comic_info == None):
        return Response("Comic does not exsist", mimetype="text/plain", status=500)
    elif(len(comic_info) == 0):
        return Response("There are no Comics", mimetype="text/plain", status=404)
    else:
        print(comic_info[0])
        for comga in comic_info:
            comga_dictionary = {
            "comgaId": comga[0],
            "type": comga[1], 
            "title": comga[2],
            "author": comga[3], 
            "cover": comga[4], 
            "artist": comga[5]}
        comga_json = json.dumps(comga_dictionary, default=str)
        return Response(comga_json, mimetype="application/json", status=201)

def create_content():
    try: 
        token = str(request.json["loginToken"])
        user_id = str(request.json["posterId"])
        read_type = str(request.json["read_type"])
        title = str(request.json["title"])
        author = str(request.json["author"])
        cover = str(request.json["cover"])
        artist = str(request.json["artist"])
        status = request.json.get("status")
        tags = request.json.get("tags")
    except IndexError:
        return Response("Data invalid", mimetype="text/plain", status=404)
    except:
        traceback.print_exc()
        print("Okay, either you don't have a login token, or this api is going crazy... or both...")
        return Response("Data Error", mimetype="text/plain", status=400)
    
    is_author = checks.check_author(token)
    if(is_author == None or "" or False):
        return Response("User not authorized to post content", mimetype="text/plain", status=401)
    elif(is_author == True):
        if((tags == None or "") and (status == None or "")):
            new_content = dbshorts.run_insertion("insert into content (read_type, title, author, cover, artist, poster_id) values (?,?,?,?,?,?)",
                                                 [read_type, title, author, cover, artist, user_id])
        elif((tags != None or "") and (status == None or "")):
            new_content = dbshorts.run_insertion("insert into content (read_type, title, author, cover, artist, tags, poster_id) values (?,?,?,?,?,?,?)",
                                                 [read_type, title, author, cover, artist, tags, user_id])
        elif((tags == None or "") and (status != None or "")):
            new_content = dbshorts.run_insertion("insert into content (read_type, title, author, cover, artist, status, poster_id) values (?,?,?,?,?,?,?)",
                                                 [read_type, title, author, cover, artist, status, user_id])
        elif((tags != None or "") and (status != None or "")):
            new_content = dbshorts.run_insertion("insert into content (read_type, title, author, cover, artist, status, tags, poster_id) values (?,?,?,?,?,?,?,?)",
                                                 [read_type, title, author, cover, artist, status, tags, user_id])

    if(new_content == None or ""):
        return Response("Database Error, something went wrong on our end, sorry mate", mimetype="text/plain", status=500)
    else:
        content_info = dbshorts.run_selection("from mvp_comga select c.id, c.read_type, c.title, c.author, c.cover, c.artist, c.status, c.tags, c.date_posted, c.poster_id from content c", [])
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
        print("SUCCESS [probably]")
        return Response(content_json, mimetype="application/json", status=201)

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
    
