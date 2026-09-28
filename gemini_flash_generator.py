from .ai_utils import ai_enabled, get_gemini_client
from .config import settings


def demo_tip(username: str, goal: str, intensity: str) -> str:
    return f"""
FITBUDDY RECOVERY & NUTRITION TIP

Hi {username}!

Your current goal is: {goal}
Training intensity: {intensity}

• Drink enough water throughout the day.
• Include protein-rich foods in your meals.
• Eat vegetables and fruits regularly.
• Get adequate sleep and recovery.
• Do not train through sharp or unusual pain.
• Increase training intensity gradually.

Consistency is more important than trying to do everything at once.
"""


def generate_tip(
    username: str,
    goal: str,
    intensity: str
) -> str:

    if not ai_enabled():
        return demo_tip(username, goal, intensity)

    try:
        client = get_gemini_client()

        prompt = f"""
You are FitBuddy, a fitness and nutrition assistant.

User:
Name: {username}
Goal: {goal}
Training intensity: {intensity}

Give a short personalized nutrition and recovery tip.

Include:
- hydration
- protein/nutrition
- sleep/recovery
- training recovery

Keep it practical and concise.
Do not provide extreme dieting advice.
"""

        response = client.models.generate_content(
            model=settings.GEMINI_TIP_MODEL,
            contents=prompt
        )

        if response and response.text:
            return response.text

    except Exception as error:
        print(f"Gemini tip generation error: {error}")

    return demo_tip(username, goal, intensity)