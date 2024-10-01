"""Human in the loop functionality"""

__all__ = [
    "HumanInTheLoop",
    "PostgresHumanInTheLoop",
]

from typing import Protocol
from psycopg_pool import ConnectionPool

from pydantic import BaseModel

from fixpoint_common.types.human import HumanTaskEntry
from fixpoint_common.workflows.human.storage_integrations.postres import (
    PostgresHumanTaskStorage,
)


class HumanInTheLoop(Protocol):
    """Human-in-the-loop client"""

    def send_task_entry(
        self,
        org_id: str,
        workflow_id: str,
        workflow_run_id: str,
        task_id: str,
        data: BaseModel,
    ) -> HumanTaskEntry:
        """Sends a task entry"""

    def get_task_entry(self, org_id: str, task_entry_id: str) -> HumanTaskEntry | None:
        """Retrieves a task"""


class PostgresHumanInTheLoop(HumanInTheLoop):
    """Human-in-the-loop client that uses Supabase"""

    _pool: ConnectionPool

    def __init__(self, pool: ConnectionPool) -> None:
        self._pool = pool

    def send_task_entry(
        self,
        org_id: str,
        workflow_id: str,
        workflow_run_id: str,
        task_id: str,
        data: BaseModel,
    ) -> HumanTaskEntry:
        """Sends a task entry"""
        task = HumanTaskEntry.from_pydantic_model(
            task_id=task_id,
            workflow_id=workflow_id,
            workflow_run_id=workflow_run_id,
            model=data,
        )
        PostgresHumanTaskStorage(self._pool).create(org_id, task)
        return task

    def get_task_entry(self, org_id: str, task_entry_id: str) -> HumanTaskEntry | None:
        """Retrieves a task"""
        return PostgresHumanTaskStorage(self._pool).get(org_id, task_entry_id)
