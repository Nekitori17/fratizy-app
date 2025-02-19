import json
import asyncio
from flask import Response
from PyCharacterAI import Client, exceptions
from werkzeug.datastructures import *

async def main(request_args: MultiDict[str, str], request_headers: Headers, request_payload: dict):
  character_account_token = request_headers.get("Authorization")
  question = request_payload.get("input")
  character_id = request_payload.get("id-character")
  voice_id = request_payload.get("id-voice")

  if not character_account_token:
    return Response(json.dumps({"error": "Unauthorized"}),status=401)
  if not character_id:
    return Response(json.dumps({"error": "Missing character id"}),status=400)

  try:
    client = Client()
    await client.authenticate(character_account_token)
    chat, getting = await client.chat.create_chat(character_id)

    response = await client.chat.send_message(character_id, chat.chat_id, question)
    result = response.get_primary_candidate().text

    return Response(json.dumps({
      "result": result,
      "getting": getting.get_primary_candidate().text
    }),
    status=200)
  except exceptions.AuthenticationError as err:
    return Response(json.dumps({"error": str(err)}), status=401)
  except exceptions.RequestError as err:
    return Response(json.dumps({"error": str(err)}), status=400)
  except Exception as err:
    return Response(json.dumps({"error": str(err)}), status=500)

def callback(request_args: MultiDict[str, str], request_headers: Headers, request_payload: dict):
  return asyncio.run(main(request_args, request_headers, request_payload))
