from typing import Optional

from sqlalchemy.orm import Session

from .models import User


def get_user(
    db: Session,
    user_id: str
) -> Optional[User]:
    return (
        db.query(User)
        .filter(User.user_id == user_id)
        .first()
    )


def get_all_users(
    db: Session
):
    return (
        db.query(User)
        .order_by(User.id.desc())
        .all()
    )


def save_user(
    db: Session,
    username: str,
    user_id: str,
    age: int,
    weight: float,
    goal: str,
    intensity: str
) -> User:

    existing_user = get_user(db, user_id)

    if existing_user:
        existing_user.username = username
        existing_user.age = age
        existing_user.weight = weight
        existing_user.goal = goal
        existing_user.intensity = intensity

        db.commit()
        db.refresh(existing_user)

        return existing_user

    user = User(
        username=username,
        user_id=user_id,
        age=age,
        weight=weight,
        goal=goal,
        intensity=intensity
    )

    db.add(user)
    db.commit()
    db.refresh(user)

    return user


def save_plan(
    db: Session,
    user_id: str,
    plan: str,
    nutrition_tip: str
) -> Optional[User]:

    user = get_user(db, user_id)

    if not user:
        return None

    user.original_plan = plan
    user.nutrition_tip = nutrition_tip

    db.commit()
    db.refresh(user)

    return user


def update_plan(
    db: Session,
    user_id: str,
    updated_plan: str,
    feedback: str
) -> Optional[User]:

    user = get_user(db, user_id)

    if not user:
        return None

    user.updated_plan = updated_plan
    user.feedback = feedback

    db.commit()
    db.refresh(user)

    return user


def get_original_plan(
    db: Session,
    user_id: str
) -> Optional[str]:

    user = get_user(db, user_id)

    if not user:
        return None

    return user.original_plan