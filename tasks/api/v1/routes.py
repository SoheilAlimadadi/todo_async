from fastapi import (
    APIRouter,
    status,
    Depends
)
from fastapi.security import OAuth2PasswordBearer

from auth.authorization import get_current_user
from .schemas import (
    TaskSchemaIn,
    TaskSchemaOut,
    TaskListSchema,
    DeleteTaskSchema
)
from auth.models import User

from tasks.repository.dal import(
    ITaskDataAccessLayer,
    TaskDataAccessLayer
)
from tasks.repository.bll import TaskService


tasks_router = APIRouter()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

@tasks_router.get(
        "/",
        status_code=status.HTTP_200_OK,
        response_model=TaskListSchema
)
async def get_tasks(
    user: User = Depends(get_current_user),
    dal : ITaskDataAccessLayer = Depends(TaskDataAccessLayer)
) -> TaskListSchema:
    """
    Retrieves the tasks associated with the authenticated user.

    Args:
        dal: (ITaskDataAccessLayer): data acess layer of task model
        user (User): The authenticated user.

    Returns:
        TaskListSchema: A list of tasks associated with the authenticated user.
    """
    tasks = await TaskService.get_tasks(dal, user)
    return TaskListSchema(tasks=tasks)

@tasks_router.post(
        "/",
        status_code=status.HTTP_201_CREATED,
        response_model=TaskSchemaOut
)
async def create_task(
    task: TaskSchemaIn,
    user: User = Depends(get_current_user),
    dal: ITaskDataAccessLayer = Depends(TaskDataAccessLayer)
) -> TaskSchemaOut:
    """
    Creates a new task associated with the authenticated user.

    Args:
        dal: (ITaskDataAccessLayer): data acess layer of task model
        task (TaskSchemaIn): The task to be created.
        user (User): The authenticated user.

    Returns:
        TaskSchemaOut: The newly created task.
    """
    task = await TaskService.create_task(
        dal,
        user,
        task.title,
        task.description
    )
    return task

@tasks_router.get(
        "/{title}",
        status_code=status.HTTP_200_OK,
        response_model=TaskSchemaOut
)
async def get_one_task(
    title: str,
    user: User= Depends(get_current_user),
    dal: ITaskDataAccessLayer = Depends(TaskDataAccessLayer)
) -> TaskSchemaOut:
    """
    Retrieves the task with the provided title associated with the
    authenticated user.

    Args:
        dal: (ITaskDataAccessLayer): data acess layer of task model
        title (str): The title of the task to be retrieved.
        user (User): The authenticated user.

    Returns:
        TaskSchemaOut: The task with the provided title associated with
        the authenticated user.
    """
    task = await TaskService.get_task(dal, user, title)
    return task

@tasks_router.patch(
        "/{title}",
        status_code=status.HTTP_200_OK,
        response_model=TaskSchemaOut
)
async def mark_task_as_complete(
    title: str,
    user: User = Depends(get_current_user),
    dal: ITaskDataAccessLayer = Depends(TaskDataAccessLayer)
) -> TaskSchemaOut:
    """
    Marks the task with the provided title associated with the
    authenticated user as complete.

    Args:
        dal: (ITaskDataAccessLayer): data acess layer of task model
        title (str): The title of the task to be marked as complete.
        user (User): The authenticated user.

    Returns:
        TaskSchemaOut: The updated task.
    """
    task = await TaskService.mark_task_as_complete(dal, user, title)
    return task

@tasks_router.delete(
        "/{title}",
        status_code=status.HTTP_200_OK,
        response_model=DeleteTaskSchema
)
async def delete_task(
    title: str,
    user: User = Depends(get_current_user),
    dal: ITaskDataAccessLayer = Depends(TaskDataAccessLayer)
) -> DeleteTaskSchema:
    """
    Deletes the task with the provided title associated with
    the authenticated user.

    Args:
        dal: (ITaskDataAccessLayer): data acess layer of task model
        title (str): The title of the task to be deleted.
        user (User): The authenticated user.

    Returns:
        DeleteTaskSchema: A message indicating whether the task
        was successfully deleted.
    """
    await TaskService.delete_task(dal, user, title)
    return DeleteTaskSchema(result="Task was Successfully deleted.")
