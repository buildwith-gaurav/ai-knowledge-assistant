from google import genai
import time

from config import GEMINI_API_KEY


client = genai.Client(api_key=GEMINI_API_KEY)



def generate_response(prompt: str) -> str:
    """Generate a response from Gemini with retry handling."""

    for attempt in range(3):
        try:
            response = client.models.generate_content(
                model="gemini-3.6-flash",
                contents=prompt
            )

            return response.text or "Gemini returned an empty response."

        except Exception as error:
            print(f"Gemini API error (attempt {attempt + 1}/3): {error}")

            if attempt < 2:
                time.sleep(2 * (attempt + 1))

    return "Gemini is temporarily unavailable. Please try again later."