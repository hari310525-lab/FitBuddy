from .ai_utils import ai_enabled, get_gemini_client
from .config import settings


def demo_workout(username: str, age: int, weight: float, goal: str, intensity: str) -> str:
    return f"""
FITBUDDY 7-DAY WORKOUT PLAN
User: {username}
Age: {age}
Weight: {weight} kg
Goal: {goal}
Intensity: {intensity}

DAY 1 - CHEST + TRICEPS
• Bench Press - 3 x 10
• Incline Dumbbell Press - 3 x 10
• Cable Fly - 3 x 12
• Triceps Pushdown - 3 x 12
• Overhead Triceps Extension - 3 x 12

DAY 2 - BACK + BICEPS
• Lat Pulldown - 3 x 10
• Seated Cable Row - 3 x 10
• One Arm Dumbbell Row - 3 x 10
• Dumbbell Curl - 3 x 12
• Hammer Curl - 3 x 12

DAY 3 - LEGS
• Squat - 3 x 10
• Leg Press - 3 x 12
• Leg Extension - 3 x 12
• Leg Curl - 3 x 12
• Standing Calf Raise - 3 x 15

DAY 4 - SHOULDERS
• Shoulder Press - 3 x 10
• Lateral Raise - 3 x 12
• Front Raise - 3 x 12
• Rear Delt Fly - 3 x 12
• Shrugs - 3 x 12

DAY 5 - FULL BODY
• Squat - 3 x 10
• Bench Press - 3 x 10
• Lat Pulldown - 3 x 10
• Dumbbell Shoulder Press - 3 x 10
• Dumbbell Curl - 3 x 12

DAY 6 - CARDIO + CORE
• Walking - 30 minutes
• Crunches - 3 x 15
• Leg Raises - 3 x 12
• Plank - 3 x 30 seconds

DAY 7 - REST
• Light walking
• Stretching
• Recovery

GENERAL GUIDELINES
• Warm up for 5-10 minutes before training.
• Use controlled movements.
• Rest 60-90 seconds between sets.
• Increase weights gradually.
• Stay hydrated.
• Sleep adequately.
"""


def generate(
    username: str,
    age: int,
    weight: float,
    goal: str,
    intensity: str
) -> str:

    # Demo mode / no API key
    if not ai_enabled():
        return demo_workout(
            username=username,
            age=age,
            weight=weight,
            goal=goal,
            intensity=intensity
        )

    try:
        client = get_gemini_client()

        prompt = f"""
You are FitBuddy, an AI fitness planning assistant.

Create a personalized 7-day workout plan.

User details:
Name: {username}
Age: {age}
Weight: {weight} kg
Goal: {goal}
Intensity: {intensity}

Requirements:
1. Create a complete 7-day plan.
2. Include exercises, sets and repetitions.
3. Include rest/recovery.
4. Include warm-up guidance.
5. Keep the plan practical for a normal gym.
6. Do not make extreme or dangerous recommendations.
7. Clearly organize Day 1 through Day 7.
8. Give general safety and recovery guidance.

Return only the workout plan.
"""

        response = client.models.generate_content(
            model=settings.GEMINI_WORKOUT_MODEL,
            contents=prompt
        )

        if response and response.text:
            return response.text

    except Exception as error:
        print(f"Gemini workout generation error: {error}")

    # If Gemini fails, the application still works
    return demo_workout(
        username=username,
        age=age,
        weight=weight,
        goal=goal,
        intensity=intensity
    )