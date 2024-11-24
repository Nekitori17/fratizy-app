from flask import Response
import json
import requests

def callback(request_args, request_headers, request_payload):
  handle_name = request_args.get("handle")
  raw_token = request_headers.get("Authorization")

  if not raw_token:
    return Response(json.dumps({"error": "Missing Authorization header"}), status=401)
  if not handle_name:
    return Response(json.dumps({"error": "Missing handle"}), status=400)
  
  # TODO: Make a phigros gamedata fetcher
  try:
    pass
  except Exception as e:
    return Response(json.dumps({"error": str(e)}), status=500)
