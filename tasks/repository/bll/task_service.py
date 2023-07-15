import logging
from datetime import datetime
from typing import List

from fastapi import (
    HTTPException,
    status
)

from tasks.repository.dal import ITaskDataAccessLayer
from auth.models import User
from tasks.models import Task


coreLogger = logging.getLogger('core')

class TaskService:
    """
    A service class that provides methods to interact with the task database.
    """

    @classmethod
    async def get_tasks(
        cls,
        dal: ITaskDataAccessLayer,
        user: User
    ) -> List[Task]:
        """
        Retrieves all tasks associated with the specified user.

        Args:
            dal (ITaskDataAccessLayer): data access layer of task model
            user (User): The user whose tasks are to be retrieved.

        Returns:
            List[Task]: A list of tasks associated with the specified user.

        Raises:
            HTTPException: If no tasks are found for the specified user.
        """
        tasks = await dal.get_all_tasks(user.username)
        if not tasks:
            coreLogger.debug(
                f"User {user.username} failed to retrieve tasks"
            )
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail='No Tasks found'
            )
        coreLogger.info(f"get all tasks was performed by user: {user.username}")
        return tasks

    @classmethod
    async def create_task(
            cls,
            dal: ITaskDataAccessLayer,
            user: User,
            title: str,
            description=None
    ) -> Task:
        """
        Creates a new task associated with the specified user.

        Args:
            dal (ITaskDataAccessLayer): data access layer of task model
            user (User): The user for whom the task is to be created.
            title (str): The title of the task to be created.
            description (Optional[str]): The description of the task to be created.

        Returns:
            Task: The newly created task.

        Raises:
            HTTPException: If a task with the same title already exists.
        """
        task = await dal.get_task(user.username, title)
        if task:
            coreLogger.debug(
                f"User {user.username} attempted to add an existing task"
            )
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail='Task with the same title already exists'
            )
        task = await dal.create_task(title, user.username, description)
        coreLogger.info(
            f'User {user.username} successfully created task {title}'
        )
        return task

    @classmethod
    async def get_task(
        cls,
        dal: ITaskDataAccessLayer,
        user: User,
        title: str
    ) -> Task:
        """
        Retrieves the task with the specified title associated with the specified user.

        Args:
            dal (ITaskDataAccessLayer): data access layer of task model
            user (User): The user for whom the task is to be retrieved.
            title (str): The title of the task to be retrieved.

        Returns:
            Task: The task with the specified title associated with the specified user.

        Raises:
            HTTPException: If the task does not exist.
        """
        task = await dal.get_task(user.username, title)
        if not task:
            coreLogger.debug(
                f"User {user.username} failed to retrieve task {title}"
            )
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail='Task does not exist'
            )
        coreLogger.info(
                f"User {user.username} succesfully to retrieved task {title}"
            )
        return task

    @classmethod
    async def delete_task(
            cls,
            dal: ITaskDataAccessLayer,
            user: User,
            title: str
    ) -> Task:
        """
        Deletes the task with the specified title associated with the specified user.

        Args:
            dal (ITaskDataAccessLayer): data access layer of task model
            user (User): The user for whom the task is to be deleted.
            title (str): The title of the task to be deleted.

        Returns:
            Task: The deleted task.

        Raises:
            HTTPException: If the task does not exist.
        """
        task = await cls.get_task(dal, user, title)
        await dal.delete_task(task)
        coreLogger.info(
                f"User {user.username} succesfully to deleted task {title}"
            )
        return task

    @classmethod
    async def mark_task_as_complete(
            cls,
            dal: ITaskDataAccessLayer,
            user: User,
            title: str
    ) -> Task:
        """
        Marks the task with the specified title associated with the
        pecified user as complete.

        Args:
            dal (ITaskDataAccessLayer): data access layer of task model
            user (User): The user for whom the task is to be marked as complete.
            title (str): The title of the task to be marked as complete.

        Returns:
            Task: The updated task.

        Raises:
            HTTPException: If the task does not exist.
        """
        task = await cls.get_task(dal, user, title)
        if task.is_completed:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail='Task is already completed.'
            )
        completed_task = await dal.update_task(
             task,
            {"is_completed": True, "completed_on": datetime.now()}
        )
        coreLogger.info(
                f"User {user.username} succesfully to completed task {title}"
            )
        return completed_task
