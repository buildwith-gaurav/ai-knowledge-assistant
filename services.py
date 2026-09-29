from google import genai

from config import GEMINI_API_KEY


client = genai.Client(api_key=GEMINI_API_KEY)


def generate_response(prompt: str) -> str:
    """Generate a response from Gemini."""

    try:
        response = client.models.generate_content(
            model="gemini-3.6-flash",
            contents=prompt
        )

        return response.text

    except Exception as error:
        print(f"Gemini API error: {error}")

        return (
            "Sorry, the AI service is temporarily unavailable. "
            "Please try again later."
        )