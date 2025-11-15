from pydantic import BaseModel

class WorkoutEntry(BaseModel):
    user_id: str
    worked_out: bool

class HabitReport(BaseModel):
    user_id: str
    streak: int
    skip_probability: float
    message: str
    history: list
