from flask import Flask, request, Response
from threading import Thread
import os
import json
import importlib
import requests

app = Flask(__name__)

@app.route("/")
def init():
  with open("pages/index.html") as f:
    return f.read()
  
@app.route("/endpoint", methods=["POST"])
def main():
  request_query = request.args.get("q")
  request_payload = request.get_json(force=True) if request.get_json() else {}

  if not request_query:
    return Response(json.dumps({"error": "No query provided"}), status=400)

  app_list_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "route")
  app_list_files = os.listdir(app_list_dir)

  app_list = [file_name[:-3] for file_name in app_list_files if file_name.endswith(".py")]
  
  if request_query not in app_list:
    return Response(json.dumps({"error": "Query not found"}), status=404)


  module = importlib.import_module(f"route.{request_query}")
  return module.callback(
    request.args,
    request.headers,
    request_payload,
  )

def run():
  app.run(host="0.0.0.0", port=8080, debug=True)

def keep_alive():
  t = Thread(target=run)
  t.start()
keep_alive()
