import json
import asyncio
from flask import Response
from PyCharacterAI import Client

async def main(request_args, request_headers, request_payload):
  character_token = request_headers.get("Authorization")
  question = request_payload.get("input")
  character_id = request_payload.get("id-character")
  voice_id = request_payload.get("id-voice")

  if not character_token:
    return Response(json.dumps({"error": "Unauthorized"}),status=401)
  if not character_id:
    return Response(json.dumps({"error": "Missing character id"}),status=400)

  try:
    client = Client()
    await client.authenticate(character_token)
    chat, getting = await client.chat.create_chat(character_id)

    response = await client.chat.send_message(character_id, chat.chat_id, question)
    result = response.get_primary_candidate().text

    return Response(json.dumps({
      "result": result,
      "getting": getting.get_primary_candidate().text
    }),
    status=200)
  except Exception as e:
    return Response(json.dumps({"error": str(e)}), status=500)

def callback(request_args, request_headers, request_payload):
  return asyncio.run(main(request_args, request_headers, request_payload))
