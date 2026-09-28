from fastapi import APIRouter, Request, Form, Depends
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session

from .database import get_db
from .models import User, Plan
from .schemas import UserInput, FeedbackRequest
from .gemini_generator import generate
from .gemini_flash_generator import generate_tip
from .updated_plan import update_plan


router = APIRouter()

# Jinja2 template configuration
templates = Jinja2Templates(directory="templates")


# =========================================================
# HOME PAGE
# =========================================================

@router.get("/", response_class=HTMLResponse)
def home(request: Request):

    return templates.TemplateResponse(
        request=request,
        name="index.html",
        context={
            "request": request
        }
    )


# =========================================================
# GENERATE WORKOUT - WEB FORM
# =========================================================

@router.post("/generate-workout", response_class=HTMLResponse)
def generate_workout(
    request: Request,
    username: str = Form(...),
    age: int = Form(...),
    weight: float = Form(...),
    goal: str = Form(...),
    intensity: str = Form(...),
    db: Session = Depends(get_db)
):

    user_id = f"user-{username.lower().replace(' ', '-')}-{age}"

    # Generate workout
    workout = generate(
        username=username,
        age=age,
        weight=weight,
        goal=goal,
        intensity=intensity
    )

    # Generate nutrition/recovery tip
    tip = generate_tip(
        username=username,
        goal=goal,
        intensity=intensity
    )

    # Check whether user already exists
    user = db.query(User).filter(
        User.user_id == user_id
    ).first()

    if not user:

        user = User(
            user_id=user_id,
            username=username,
            age=age,
            weight=weight,
            goal=goal,
            intensity=intensity
        )

        db.add(user)
        db.commit()
        db.refresh(user)

    # Save workout plan
    plan = Plan(
        user_id=user.id,
        original_plan=workout,
        updated_plan=None,
        nutrition_tip=tip,
        feedback=None
    )

    db.add(plan)
    db.commit()
    db.refresh(plan)

    return templates.TemplateResponse(
        request=request,
        name="result.html",
        context={
            "request": request,
            "user": user,
            "plan": plan,
            "workout": workout,
            "tip": tip
        }
    )


# =========================================================
# SUBMIT FEEDBACK
# =========================================================

@router.post("/submit-feedback", response_class=HTMLResponse)
def submit_feedback(
    request: Request,
    user_id: str = Form(...),
    feedback: str = Form(...),
    db: Session = Depends(get_db)
):

    user = db.query(User).filter(
        User.user_id == user_id
    ).first()

    if not user:

        return RedirectResponse(
            url="/",
            status_code=303
        )

    # Get latest plan
    plan = (
        db.query(Plan)
        .filter(Plan.user_id == user.id)
        .order_by(Plan.created_at.desc())
        .first()
    )

    if not plan:

        return RedirectResponse(
            url="/",
            status_code=303
        )

    current_plan = (
        plan.updated_plan
        or plan.original_plan
    )

    # Generate updated workout
    new_plan = update_plan(
        original_plan=current_plan,
        feedback=feedback,
        goal=user.goal,
        intensity=user.intensity
    )

    plan.feedback = feedback
    plan.updated_plan = new_plan

    db.commit()
    db.refresh(plan)

    return templates.TemplateResponse(
        request=request,
        name="result.html",
        context={
            "request": request,
            "user": user,
            "plan": plan,
            "workout": new_plan,
            "tip": plan.nutrition_tip
        }
    )


# =========================================================
# VIEW ALL USERS
# =========================================================

@router.get("/view-all-users", response_class=HTMLResponse)
def view_all_users(
    request: Request,
    db: Session = Depends(get_db)
):

    users = (
        db.query(User)
        .order_by(User.created_at.desc())
        .all()
    )

    return templates.TemplateResponse(
        request=request,
        name="all_users.html",
        context={
            "request": request,
            "users": users
        }
    )


# =========================================================
# DELETE USER
# =========================================================

@router.post("/delete-user/{user_id}")
def delete_user(
    user_id: str,
    db: Session = Depends(get_db)
):

    user = db.query(User).filter(
        User.user_id == user_id
    ).first()

    if user:

        db.delete(user)
        db.commit()

    return RedirectResponse(
        url="/view-all-users",
        status_code=303
    )


# =========================================================
# HEALTH CHECK
# =========================================================

@router.get("/api/health")
def health():

    return {
        "status": "ok",
        "app": "FitBuddy"
    }


# =========================================================
# API - GENERATE WORKOUT
# =========================================================

@router.post("/api/generate-workout")
def api_generate_workout(
    data: UserInput
):

    workout = generate(
        username=data.username,
        age=data.age,
        weight=data.weight,
        goal=data.goal,
        intensity=data.intensity
    )

    tip = generate_tip(
        username=data.username,
        goal=data.goal,
        intensity=data.intensity
    )

    return {
        "user": data.model_dump(),
        "workout": workout,
        "nutrition_tip": tip
    }


# =========================================================
# API - FEEDBACK
# =========================================================

@router.post("/api/feedback")
def api_feedback(
    data: FeedbackRequest
):

    return {
        "status": "received",
        "user_id": data.user_id,
        "feedback": data.feedback
    }