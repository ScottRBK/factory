"""The Definition of Done agreement as a Markdown file in the workspace."""
from pathlib import Path

from forgetful_factory.shared.resource_files import check_skill_file, write_new


class MarkdownAgreement:
    def __init__(self, workspace: Path):
        self.path = workspace / '.factory/definition_of_done.md'

    @property
    def location(self) -> str:
        return str(self.path)

    def found(self) -> bool:
        if self.path.exists() or self.path.is_symlink():
            check_skill_file(self.path)
            return True
        return False

    def write(self, text: str) -> None:
        write_new(self.path, text)

    def read(self) -> str:
        return self.path.read_text(encoding='utf-8')
