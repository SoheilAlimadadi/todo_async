from typing import Optional, List
from datetime import datetime

from pydantic import BaseModel

class TaskSchemaOut(BaseModel):
    """
    A Pydantic model representing a task object in the response body.

    Attributes:
        title (str): The title of the task.
        description (Optional[str]): The description of the task.
        is_completed (bool): Whether the task is completed or not.
        user (str): The email of the user who created the task.
        created (datetime): The date and time when the task was created.
        completed_on (Optional[datetime]): The date and time when the task
        was completed, if it is completed.
    """
    title: str
    description: Optional[str]
    is_completed: bool
    user: str
    created: datetime
    completed_on: Optional[datetime]

class TaskSchemaIn(BaseModel):
    """
    A Pydantic model representing a task object in the request body.

    Attributes:
        title (str): The title of the task.
        description (Optional[str]): The description of the task.
    """
    title: str
    description: Optional[str] = None

class UserSchema(BaseModel):
    """
    A Pydantic model representing a user object.

    Attributes:
        email (str): The email address of the user.
    """
    email: str

class TaskListSchema(BaseModel):
    """
    A Pydantic model representing a list of tasks in the response body.

    Attributes:
        tasks (List[TaskSchemaOut]): A list of tasks.
    """
    tasks: List[TaskSchemaOut]

class DeleteTaskSchema(BaseModel):
    """
    A Pydantic model representing the response body when a task is deleted.

    Attributes:
        result (str): A message indicating whether the task was successfully deleted.
    """
    result: str
