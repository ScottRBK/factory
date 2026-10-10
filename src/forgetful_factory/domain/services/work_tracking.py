from typing import Protocol

from forgetful_factory.domain.models import Label, WorkSource


class WorkTrackingService(Protocol):
    def check_access(self, source: WorkSource) -> None: ...

    def list_labels(self, source: WorkSource) -> tuple[Label, ...]: ...

    def create_label(self, source: WorkSource, label: Label) -> None: ...
