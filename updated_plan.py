from .ai_utils import ai_enabled, get_gemini_client
from .config import settings


def demo_updated_plan(
    original_plan: str,
    feedback: str,
    goal: str,
    intensity: str
) -> str:

    return f"""
UPDATED FITBUDDY WORKOUT PLAN

Goal: {goal}
Intensity: {intensity}

Your feedback:
{feedback}

The workout has been adjusted based on your feedback.

{original_plan}

ADJUSTMENT NOTES
• Reduce the weight if the previous workout was too difficult.
• Increase rest time when necessary.
• Maintain correct exercise form.
• Progress gradually.
• Take recovery seriously.
"""


def update_plan(
    original_plan: str,
    feedback: str,
    goal: str,
    intensity: str
) -> str:

    if not ai_enabled():
        return demo_updated_plan(
            original_plan=original_plan,
            feedback=feedback,
            goal=goal,
            intensity=intensity
        )

    try:
        client = get_gemini_client()

        prompt = f"""
You are FitBuddy, an AI fitness assistant.

The user has an existing workout plan.

GOAL:
{goal}

INTENSITY:
{intensity}

EXISTING PLAN:
{original_plan}

USER FEEDBACK:
{feedback}

Create a revised complete 7-day workout plan.

Requirements:
1. Consider the user's feedback.
2. Keep the user's goal in mind.
3. Maintain appropriate training intensity.
4. Include exercises, sets and repetitions.
5. Include recovery/rest.
6. Clearly organize Day 1 through Day 7.
7. Do not recommend dangerous or extreme training.
8. Return only the revised plan.
"""

        response = client.models.generate_content(
            model=settings.GEMINI_WORKOUT_MODEL,
            contents=prompt
        )

        if response and response.text:
            return response.text

    except Exception as error:
        print(f"Gemini plan update error: {error}")

    return demo_updated_plan(
        original_plan=original_plan,
        feedback=feedback,
        goal=goal,
        intensity=intensity
    )