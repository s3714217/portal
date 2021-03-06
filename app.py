from flask import *
from flask_restful import Api
from resources.db import *
from resources.translate import translate_util
from datetime import datetime
from resources.translate import Translate
import requests
from flask import request
from flask import copy_current_request_context
app = Flask(__name__)
api = Api(app)

api.add_resource(Translate, "/api/translate/word=<string:word>&language=<string:language>")

@app.route("/")
def index():
  title = "My App"
  return render_template("index.html",title=title)

@app.route("/api/translate")
def translate_api():
  code_list = translate_util().get_code_list()
  return render_template("translate.html", code_list= code_list)

@app.route("/api/encrypt")
def encrypt_api():
  return render_template("encrypt.html")

@app.route("/api")
def api_menu():
  return render_template("api_menu.html")

@app.route("/guestbook")
def guestbook():
  message = GuestBookDatabase().get_guestbook_message()
  if len(message) < 1:
    return render_template("guestbook.html", empty=True)
  else:
    return render_template("guestbook.html", empty=False, message=message)

@app.route("/guestbook", methods=['POST'])
def parse_guestbook_request():
    new_message = []
    new_message.append(datetime.now())
    if request.method == 'POST':
      if request.form['name'] == '':
        new_message.append("Unknow user")
      else:
        new_message.append(request.form['name']) 
      new_message.append(request.form['message'])
    GuestBookDatabase().new_guestbook_message(new_message)
    return render_template("guestbook.html", empty=False,message=GuestBookDatabase().get_guestbook_message())

@app.route("/api/translate", methods=['POST'])
def parse_translate_request():
  if request.method == 'POST':
    
    response = requests.get(request.url + f"/word={request.form['word']}&language={request.form['language']}")
    
    if response.status_code == 200:
      return str(response.json())
    else:
      return f"Invalid word."

@app.route('/api/authentication', methods=['POST'])
def create_task():
    if not 'username' in request.json or not 'password' in request.json or not 'token' in request.json:
      return "Invalid request"
    return request.json['username']

if __name__ == "__main__":
  app.run(debug=True)