from flask import Response
import google.generativeai as gen_ai
from utils.get_timestamp import *
import json

def callback(request_args, request_headers, request_payload):
  gemini_token = request_headers.get("Authorization")
  question = request_payload.get("input")
  ai_model = request_payload.get("model")

  if not gemini_token:
    return Response(json.dumps({"error": "Missing Authorization header"}), status=401)
  if not ai_model:
    return Response(json.dumps({"error": "Missing model parameter"}), status=400)
  if not question:
    return Response(json.dumps({"error": "Missing input parameter"}), status=400)

  generation_configs = {
    "temperature": 1,
    "top_p": 0.95,
    "top_k": 64,
    "max_output_tokens": 8192,
    "response_mime_type": "text/plain",
  }
  safety_settings = [
    {
      "category": "HARM_CATEGORY_HARASSMENT",
      "threshold": "BLOCK_NONE",
    },
    {
      "category": "HARM_CATEGORY_HATE_SPEECH",
      "threshold": "BLOCK_NONE",
    },
    {
      "category": "HARM_CATEGORY_SEXUALLY_EXPLICIT",
      "threshold": "BLOCK_NONE",
    },
    {
      "category": "HARM_CATEGORY_DANGEROUS_CONTENT",
      "threshold": "BLOCK_NONE",
    }
  ]

  try:
    gen_ai.configure(api_key=gemini_token)
    model = gen_ai.GenerativeModel(
      model_name=ai_model,
      safety_settings=safety_settings,
      generation_config=generation_configs,
    )

    response = model.generate_content(question)

    return Response(json.dumps({
      "output": response.text,
      "timestamp": get_timestamp(request_payload.get("timezone")),
      }),
      status=200
    )
  except Exception as e:
    return Response(json.dumps({"error": str(e)}), status=500)
