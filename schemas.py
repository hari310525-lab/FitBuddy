from pydantic import BaseModel, Field


class UserInput(BaseModel):
    user_id: str = Field(default="user-001")
    username: str = Field(min_length=2, max_length=50)
    age: int = Field(ge=13, le=100)
    weight: float = Field(gt=20, lt=300)
    goal: str = Field(min_length=2, max_length=100)
    intensity: str = Field(default="moderate", max_length=50)


class FeedbackRequest(BaseModel):
    user_id: str
    feedback: str = Field(min_length=2, max_length=2000)