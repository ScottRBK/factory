"""Promises every PlanStore adapter keeps. Plans and tasks stay plain dicts."""


class PlanStoreContract:
    """Mix into unittest.TestCase. The subclass supplies a store for project_id."""

    project_id: int

    def store(self):
        raise NotImplementedError

    def create(self, store, reference='tracker:platform#ENG-7'):
        store.create_plan(title='Add a habitat', external_ref=reference,
                          source_url='https://tracker.example/ENG-7', context='{}')
        plan, = store.plans(reference)
        return plan

    def test_created_plan_is_in_the_project_and_found_by_reference(self):
        store = self.store()
        summary = self.create(store)
        plan = store.get_plan(summary['id'])
        self.assertTrue(store.owns(plan))
        self.assertEqual(plan['external_ref'], 'tracker:platform#ENG-7')
        self.assertEqual(store.plans('tracker:platform#OTHER-1'), [])
        self.assertEqual(len(store.plans()), 1)

    def test_plan_of_another_project_is_not_owned(self):
        store = self.store()
        self.assertFalse(store.owns({'id': 1, 'project_id': self.project_id + 1}))
        self.assertFalse(store.owns({'id': 1}))

    def test_updates_plans_and_tasks(self):
        store = self.store()
        plan_id = self.create(store)['id']
        store.update_plan(plan_id, context='{"ownership_create_started": true}')
        store.create_task(plan_id=plan_id, title='Feature ownership', description='{}')
        task, = store.tasks(plan_id)
        store.update_task(task['id'], description='{"kind": "factory-ownership"}')
        self.assertEqual(store.get_plan(plan_id)['context'], '{"ownership_create_started": true}')
        task, = store.tasks(plan_id)
        self.assertEqual(task['description'], '{"kind": "factory-ownership"}')

    def test_backend_identity_is_stable_text(self):
        first, second = self.store().backend_identity(), self.store().backend_identity()
        self.assertIsInstance(first, str)
        self.assertTrue(first)
        self.assertEqual(first, second)
