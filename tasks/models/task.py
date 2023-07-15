from datetime import datetime
from typing import Optional

from pydantic import (
    Field,
    EmailStr
)
from beanie import (
    Document,
    before_event,
    Insert
)


class Task(Document):
    """
    A Pydantic model representing a task object in the database.

    Attributes:
        title (str): The title of the task.
        description (Optional[str]): The description of the task.
        is_completed (bool): Whether the task is completed or not.
        user (EmailStr): The email address of the user who created the task.
        created (datetime): The date and time when the task was created.
        completed_on (Optional[datetime]): The date and time when the task
        was completed, if it is completed.
    """
    title: str = Field(
        min_length=4,
        max_length=150,
        description="Title of the task",
    )
    description: Optional[str] = Field(
        default=None,
        description="Description of the task"
    )
    is_completed: bool = Field(
        default=False,
        description="Whether the task is completed or not"
    )
    user: EmailStr = Field(
        description="Email of the user who created this task"
    )
    created: datetime = Field(
        description="Task creation time"
    )
    completed_on: Optional[datetime] = None

    class Settings:
        name = "tasks"
        validate_on_save = True

    @before_event(Insert)
    def completed_on(self):
        self.created = datetime.now()

    @before_event(Insert)
    def lower_name(self):
        self.title = self.title.lower()

    def __str__(self):
        return f"{self.title}"

    def __repr__(self):
        return f"<task: {self.title} - user: {self.user}>"
