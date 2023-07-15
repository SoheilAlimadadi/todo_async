from typing import List
from datetime import datetime

from .interface import ITaskDataAccessLayer
from tasks.models import Task


class TaskDataAccessLayer(ITaskDataAccessLayer):
    """
    A data access layer class that provides methods to interact with the task database.
    """
    async def get_all_tasks(self, user: str) -> List[Task]:
        """
        Retrieves all tasks associated with the specified user.

        Args:
            user (str): The user whose tasks are to be retrieved.

        Returns:
            List[Task]: A list of tasks associated with the specified user.
        """
        return await Task.find(Task.user == user).to_list()

    async def get_task(self, user: str, title: str) -> Task:
        """
        Retrieves the task with the specified title associated with the specified user.

        Args:
            user (str): The user for whom the task is to be retrieved.
            title (str): The title of the task to be retrieved.

        Returns:
            Task: The task with the specified title associated with the specified user.
        """
        return await Task.find_one(
            Task.title == title,
            Task.user == user
        )

    async def create_task(
            self, title: str,
            user: str,
            description=None
    ) -> Task:
        """
        Creates a new task associated with the specified user.

        Args:
            title (str): The title of the task to be created.
            user (str): The user for whom the task is to be created.
            description (Optional[str]): The description of the task to be created.

        Returns:
            Task: The newly created task.
        """
        task = Task(
            title=title,
            description=description,
            is_completed=False,
            user=user,
            created=datetime.now(),
            completed_on=None
        )
        return await task.insert()

    async def delete_task(self, task: Task) -> bool:
        """
        Deletes the specified task.

        Args:
            task (Task): The task to be deleted.

        Returns:
            bool: True if the task was successfully deleted, False otherwise.
        """
        return await task.delete()

    async def update_task(self, task: Task, fields: dict) -> Task:
        """
        Updates the specified task with the specified fields.

        Args:
            task (Task): The task to be updated.
            fields (dict): A dictionary of fields to be updated and their new values.

        Returns:
            Task: The updated task.
        """
        return await task.update({"$set": fields})
