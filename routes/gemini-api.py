import json
from pathlib import Path
from flask import Response
from utils.get_timestamp import *
import google.generativeai as gen_ai
from google.api_core import exceptions
from google.generativeai import types
from werkzeug.datastructures import *

def callback(request_args: MultiDict[str, str], request_headers: Headers, request_payload: dict):
  gemini_token = request_headers.get("Authorization")
  prompt = request_payload.get("input")
  ai_model = request_payload.get("model")
  system_instruction = request_payload.get("instruction")

  if not gemini_token:
    return Response(json.dumps({"error": "Missing Authorization header"}), status=401)
  if not ai_model:
    return Response(json.dumps({"error": "Missing model parameter"}), status=400)
  if not prompt:
    return Response(json.dumps({"error": "Missing input parameter"}), status=400)

  generation_config: types.GenerationConfigType = {
    "temperature": 2,
    "top_p": 0.95,
    "top_k": 64,
    "max_output_tokens": 65536,
    "response_mime_type": "text/plain",
  }

  safety_settings: list[types.SafetySettingDict] = [
    {
      "category": types.HarmCategory.HARM_CATEGORY_HARASSMENT,
      "threshold": types.HarmBlockThreshold.BLOCK_NONE
    },
    {
      "category": types.HarmCategory.HARM_CATEGORY_HATE_SPEECH,
      "threshold": types.HarmBlockThreshold.BLOCK_NONE
    },
    {
      "category": types.HarmCategory.HARM_CATEGORY_SEXUALLY_EXPLICIT,
      "threshold": types.HarmBlockThreshold.BLOCK_NONE
    },
    {
      "category": types.HarmCategory.HARM_CATEGORY_DANGEROUS_CONTENT,
      "threshold": types.HarmBlockThreshold.BLOCK_NONE
    }
  ]
  try:
    gen_ai.configure(api_key=gemini_token)
    model = gen_ai.GenerativeModel(
      model_name=ai_model,
      safety_settings=safety_settings,
      generation_config=generation_config,
      system_instruction=system_instruction
    )

    response = model.generate_content(prompt)
    response_dict: types.GenerateContentResponse = {
      "text": response.text,
      "model_version": response.model_version,
      "usage_metadata": {
        "cached_content_token_count": response.usage_metadata.cached_content_token_count,
        "candidates_token_count": response.usage_metadata.candidates_token_count,
        "prompt_token_count": response.usage_metadata.prompt_token_count,
        "total_token_count": response.usage_metadata.total_token_count
      },
      "timestamp": get_timestamp()
    }

    return Response(json.dumps(response_dict), status=200)
  
  except exceptions.BadRequest as err:
    return Response(json.dumps({"error": str(err)}), status=400)
  except exceptions.BadGateway as err:
    return Response(json.dumps({"error": str(err)}), status=502)
  except exceptions.TooManyRequests as err:
    return Response(json.dumps({"error": str(err)}), status=429)
  except exceptions.Forbidden as err:
    return Response(json.dumps({"error": str(err)}), status=403)
  except exceptions.GatewayTimeout as err:
    return Response(json.dumps({"error": str(err)}), status=504)
  except exceptions.Unauthenticated as err:
    return Response(json.dumps({"error": str(err)}), status=401)
  except exceptions.NotFound as err:
    return Response(json.dumps({"error": str(err)}), status=404)
  except exceptions.Unauthorized as err:
    return Response(json.dumps({"error": str(err)}), status=401)
  except Exception as err:
    return Response(json.dumps({"error": str(err)}), status=500)
