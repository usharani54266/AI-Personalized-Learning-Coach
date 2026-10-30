

import os
import json
import time

from dotenv import load_dotenv
from google import genai
from google.genai import types

load_dotenv(override=True)

API_KEY = os.getenv("GEMINI_API_KEY")
MODEL_NAME = os.getenv(
    "GEMINI_MODEL",
    "gemini-3.8-flash"
)


# ----------------------------------
# CREATE GEMINI CLIENT
# ----------------------------------

def get_gemini_client():

    if not API_KEY:
        raise ValueError(
            "Gemini API key not found. Check your .env file."
        )

    return genai.Client(api_key=API_KEY)


# ----------------------------------
# GENERATE JSON WITH AUTOMATIC RETRIES
# ----------------------------------

def generate_json(prompt):

    client = get_gemini_client()

    max_attempts = 3

    for attempt in range(max_attempts):

        try:

            response = client.models.generate_content(
                model=MODEL_NAME,
                contents=prompt,
                config=types.GenerateContentConfig(
                    response_mime_type="application/json",
                    temperature=0.3
                )
            )

            if not response.text:
                raise ValueError(
                    "Gemini returned an empty response."
                )

            try:
                return json.loads(response.text)

            except json.JSONDecodeError as error:
                raise ValueError(
                    "Gemini returned invalid JSON."
                ) from error

        except Exception as error:

            error_message = str(error).upper()

            temporary_error = (
                "503" in error_message
                or "UNAVAILABLE" in error_message
                or "429" in error_message
                or "RESOURCE_EXHAUSTED" in error_message
            )

            if temporary_error and attempt < max_attempts - 1:

                wait_time = 2 ** (attempt + 1)

                print(
                    f"Gemini is busy. Retrying in {wait_time} seconds..."
                )

                time.sleep(wait_time)

            else:
                raise
