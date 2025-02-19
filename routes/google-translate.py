import json
import asyncio
from flask import Response
from googletrans import Translator, LANGCODES
from werkzeug.datastructures import *

async def main(request_args: MultiDict[str, str], request_headers: Headers, request_payload: dict):
  target_language = request_payload.get("lang")
  message_content = request_payload.get("input")
  
  if not target_language or not message_content:
    return Response(json.dumps({"error": "Missing parameters"}), status=400)
  if target_language not in LANGCODES.values():
    return Response(json.dumps({"error": "Invalid language"}), status=400)

  try:
    async with Translator() as translator:
      translation = await translator.translate(message_content, dest=target_language)
    
      return Response(json.dumps({"result": translation.text}))
  except Exception as e:
    return Response(json.dumps({"error": str(e)}), status=500)
  
def callback(request_args: MultiDict[str, str], request_headers: Headers, request_payload: dict):
  return asyncio.run(main(request_args, request_headers, request_payload))