from google import genai

from .config import settings


def ai_enabled() -> bool:
    """
    Check whether Gemini AI is enabled.
    """

    if settings.AI_MODE.lower() == "demo":
        return False

    if not settings.GOOGLE_API_KEY:
        return False

    return True


def get_gemini_client():
    """
    Create and return the Google Gemini client.
    """

    if not settings.GOOGLE_API_KEY:
        raise RuntimeError(
            "GOOGLE_API_KEY is missing from the .env file."
        )

    return genai.Client(
        api_key=settings.GOOGLE_API_KEY
    )