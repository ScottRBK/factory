"""Promises every AgreementStore adapter keeps about the Definition of Done agreement.

A new agreement store is done when a subclass of AgreementStoreContract passes for it.
"""


class AgreementStoreContract:
    """Mix into unittest.TestCase. The subclass supplies a store for an empty workspace."""

    def store(self):
        raise NotImplementedError

    def test_empty_workspace_has_no_agreement(self):
        store = self.store()
        self.assertFalse(store.found())
        self.assertTrue(store.location)

    def test_written_agreement_is_found_and_read_back(self):
        store = self.store()
        store.write('# Definition of Done\n\nAfter merge.\n')
        self.assertTrue(self.store().found())
        self.assertEqual(self.store().read(), '# Definition of Done\n\nAfter merge.\n')

    def test_writing_again_never_replaces_the_saved_agreement(self):
        self.store().write('# Agreed by people\n')
        self.store().write('# Proposed later\n')
        self.assertEqual(self.store().read(), '# Agreed by people\n')
