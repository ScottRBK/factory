"""Promises every PlanStore and PlanningSetup adapter keeps. Plans and tasks stay dicts."""

from forgetful_factory.shared.errors import FactoryError


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


class PlanningSetupContract:
    """Mix into unittest.TestCase. The subclass supplies the adapter and a connection to it."""

    def setup(self):
        raise NotImplementedError

    def connection(self, project_id=None):
        raise NotImplementedError

    def test_created_project_is_listed(self):
        setup = self.setup()
        before = setup.projects(self.connection())
        project_id = setup.create_project(self.connection(), 'Dino habitat')
        listed = {project['id']: project['name'] for project in setup.projects(self.connection())}
        self.assertIsInstance(project_id, int)
        self.assertEqual(listed.get(project_id), 'Dino habitat')
        self.assertEqual(len(listed), len(before) + 1)

    def test_check_confirms_access_to_the_selected_project(self):
        setup = self.setup()
        project_id = setup.create_project(self.connection(), 'Dino habitat')
        message = setup.check(self.connection(project_id), execution_enabled=True)
        self.assertIsInstance(message, str)
        self.assertTrue(message)

    def test_check_refuses_a_connection_without_a_project(self):
        with self.assertRaises(FactoryError):
            self.setup().check(self.connection(), execution_enabled=False)

    def test_prepare_can_repeat(self):
        setup = self.setup()
        setup.prepare(self.connection())
        setup.prepare(self.connection())

    def test_browser_login_need_is_yes_or_no(self):
        self.assertIsInstance(self.setup().uses_browser_login(self.connection()), bool)
