from typing import Protocol

from forgetful_factory.shared.errors import FactoryError


class PlanningReadError(FactoryError):
    """A native read failed or cannot establish a complete inventory or record identity."""


class PlanStore(Protocol):
    """The factory's plans and tasks in one project of one store. Records stay dicts."""

    def check(self) -> None: ...

    def plans(self, external_ref: str | None = None) -> list[dict]: ...

    def get_plan(self, plan_id: int) -> dict: ...

    def create_plan(self, **fields) -> dict:
        """Create a plan in the factory's project; the store adds the project itself."""

    def update_plan(self, plan_id: int, **fields) -> dict: ...

    def tasks(self, plan_id: int) -> list[dict]: ...

    def create_task(self, **fields) -> dict: ...

    def update_task(self, task_id: int, **fields) -> dict: ...

    def owns(self, plan: dict) -> bool:
        """Whether a plan record belongs to the factory's project."""

    def backend_identity(self) -> str:
        """Stable text naming this store, saved in cleanup receipts."""
