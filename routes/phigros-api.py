import json
from flask import Response
from PhigrosAPILib import PhigrosAPI
from werkzeug.datastructures import *

def callback(request_args: MultiDict[str, str], request_headers: Headers, request_payload: dict):
  handle_name = request_args.get("handle")
  session_token = request_headers.get("Authorization")
  overflow = int(request_payload.get("overflow")) or 0

  if not session_token:
    return Response(json.dumps({"error": "Missing Authorization header"}), status=401)
  if not handle_name:
    return Response(json.dumps({"error": "Missing handle"}), status=400)
  
  try:
    client = PhigrosAPI(session_token)
    response = None

    if handle_name == "user":
      response = client.user_info
    elif handle_name == "summary":
      response = client.player_summary
    elif handle_name == "records":
      response = client.get_records(overflow)
    elif handle_name == "bests":
      response = client.get_best_records(int(overflow))
    else:
      return Response(json.dumps({"error": "Invalid handle"}), status=400)

    return Response(json.dumps(response), status=200)
  except Exception as e:
    return Response(json.dumps({"error": str(e)}), status=500)
