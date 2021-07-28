from dbcuts import dbshorts
import traceback
from flask import Response
import json

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
            "title": comga[1], 
            "title": comga[2],
            "author": comga[3], 
            "cover": comga[4], 
            "artist": comga[5]}
        comga_json = json.dumps(comga_dictionary, default=str)
        return Response(comga_json, mimetype="application/json", status=201)
