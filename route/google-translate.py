import json
from flask import Response
from googletrans import Translator

def callback(request_args, request_headers, request_payload):
  target_language = request_payload.get("lang")
  message_content = request_payload.get("input")
  
  if not target_language or not message_content:
    return Response(json.dumps({"error": "Missing parameters"}), status=400)

  
  try:
    translator = Translator()
    translation = translator.translate(message_content, dest=target_language)
    
    return Response(json.dumps({"result": translation.text}))
  except Exception as e:
    return Response(json.dumps({"error": str(e)}), status=500)