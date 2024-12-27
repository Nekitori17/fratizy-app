from flask import Flask, request, Response
import os
import json
import importlib

app = Flask(__name__)

@app.route("/")
def init():
  with open("pages/index.html") as f:
    return f.read()
  
@app.route("/endpoint", methods=["POST"])
def main():
  request_query = request.args.get("q")
  request_payload = json.loads(request.data.decode("utf-8")) if request.data else {}

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

if __name__ == "__main__":
  app.run(host="0.0.0.0", port=8080, debug=True)
