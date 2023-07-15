from abc import ABC, abstractmethod
from typing import List

from tasks.models import Task


class ITaskDataAccessLayer(ABC):

    @abstractmethod
    async def get_all_tasks(self, user: str) -> List[Task]:
        raise NotImplementedError

    @abstractmethod
    async def get_task(self, user: str, title: str) -> Task:
        raise NotImplementedError

    @abstractmethod
    async def create_task(self, title: str, user: str, description=None) -> Task:
        raise NotImplementedError

    @abstractmethod
    async def delete_task(self, task: Task) -> bool:
        raise NotImplementedError

    @abstractmethod
    async def update_task(self, task: Task, fields: dict) -> Task:
        raise NotImplementedError
