from flask import Response
import urllib.parse
import json

def callback(request_args, request_headers, request_payload):
  input_data = {
    "background": request_payload.get("background"),
    "title": request_payload.get("title"),
    "body": request_payload.get("body"),
    "footer": request_payload.get("footer"),
    "avatar": request_payload.get("avatar")
  }

  output_data = {}
  for key, value in input_data.items():
    if value is not None:
      output_data[key] = urllib.parse.quote(value.strip())
    else:
      return Response(json.dumps({
        "error": "Missing required parameter"
        }), status=400)
  
  link_output = (f"https://api.popcat.xyz/welcomecard?background={output_data['background']}&text1={output_data['title']}&text2={output_data['body']}&text3={output_data['footer']}&avatar={output_data['avatar']}")
    
  return Response(json.dumps({"link": link_output}), status=200)
