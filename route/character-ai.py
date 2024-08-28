from flask import Response
from PyCharacterAI import Client
import json
import asyncio

async def main(request_args, request_headers, request_payload):
  character_token = request_headers.get("Authorization")
  question = request_payload.get("input")
  character_id = request_payload.get("id-character")
  voice_id = request_payload.get("id-voice")

  if not character_token:
    return Response(json.dumps({"error": "Unauthorized"}),status=401)
  if not character_id:
    return Response(json.dumps({"error": "Missing character id"}),status=400)

  result = {}
  client = Client()
  await client.authenticate_with_token(character_token)
  chat = client.create_or_continue_chat(character_id)

  result["message"] = await chat.send_

def callback(request_args, request_headers, request_payload):
  return asyncio.run(main(request_args, request_headers, request_payload))
