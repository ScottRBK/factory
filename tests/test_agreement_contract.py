"""Run the AgreementStore contract against the Markdown agreement file."""
import tempfile
import unittest
from pathlib import Path

from contracts.factory import AgreementStoreContract

from forgetful_factory.factory.adapters.markdown_agreement import MarkdownAgreement


class MarkdownAgreementContractTests(AgreementStoreContract, unittest.TestCase):
    def setUp(self):
        temporary = tempfile.TemporaryDirectory()
        self.addCleanup(temporary.cleanup)
        self.workspace = Path(temporary.name)

    def store(self):
        return MarkdownAgreement(self.workspace)
