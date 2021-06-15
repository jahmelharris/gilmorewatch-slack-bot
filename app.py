import urllib
import os
from flask import abort, Flask, jsonify, request
import sys
import urllib.parse
import urllib.request

import json

app = Flask(__name__)
lines = []
currentLine = 0
f=None
print(currentLine)
def is_request_valid(request):
    is_token_valid = request.values['token'] == ""#os.environ['SLACK_VERIFICATION_TOKEN']
    is_team_id_valid = request.form['team_id'] == "" #os.environ['SLACK_TEAM_ID']

    return is_token_valid and is_team_id_valid

def returnNextFiveLines():
    global currentLine
    global f
    global lines
    print(lines)
    if(f==None):
        return "choose an episode, dingus"
    data = ""
    for x in range(5):
        print(currentLine)
        if(currentLine < len(lines)):
            data = data+lines[currentLine]
            currentLine+=1
        else:
            data = data+"That's all folks"
            f.close()
            f=None
            lines=[]
            break
    return data

@app.route('/getEpisode', methods=['POST'])
def hello_there():
    if not is_request_valid(request):
        abort(400)
    global lines
    global currentLine
    global f
    print(request.values)
    print(request.values['text'])
    text = request.values['text']
    if text != "next":
        if(f != None):
            f.close()
        lines=[]
        eps=text.split()
        try:
            season=str(int(eps[0])-1)
            episode=str(int(eps[1])) #just check its actually a number and not someone trying to do dir traversal
        except:
            return jsonify(response_type='in_channel',text="Arguments not understood :/")
        quality="low"
        print("gonna start a new episode");
        currentLine = 0
        try:
            filename=season+episode+quality
            print("filename"+filename)
            f = open(filename)
        except:
            return jsonify(response_type='in_channel',text="Sorry. Episode cannot be found")
        lines = f.readlines()
        print(lines)
    data = returnNextFiveLines()
    return jsonify(response_type='in_channel',text=data)
