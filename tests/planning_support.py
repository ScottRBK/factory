"""Controlled native Forgetful program protocol; no service or credentials involved."""
PLANNING = '''
    if (args[:1] == ['call']
            and args[1] not in ('get_project', 'get_current_user', 'create_project')):
        tool = args[1]
        values = json.loads(args[args.index('--args') + 1])
        state_path = Path(os.environ.get('PLANNING_STATE', Path.cwd() / 'fixture-plans.json'))
        import fcntl
        lock = state_path.with_suffix('.lock').open('a')
        fcntl.flock(lock, fcntl.LOCK_EX)
        def save_planning_state():
            replacement = state_path.with_suffix('.next')
            replacement.write_text(json.dumps(state))
            replacement.replace(state_path)
        state = json.loads(state_path.read_text()) if state_path.exists() else {
            'plans': [], 'tasks': [], 'calls': []}
        state['calls'].append([tool, values])
        if (tool in ('create_plan', 'update_plan')
                and values.get('context') is not None and len(values['context']) > 2000):
            error = 'plan.context exceeds 2000 characters'
            state.setdefault('rejections', []).append(error)
            save_planning_state()
            sys.exit(error)
        if tool == 'list_plans':
            assert set(values) <= {'external_ref'}, values
            rows = [p for p in state['plans'] if not values or
                    p['external_ref'] == values['external_ref']]
            result = {'plans': rows, 'total_count': len(rows)}
        elif tool == 'query_tasks':
            assert set(values) == {'plan_id'}, values
            rows = [t for t in state['tasks'] if t['plan_id'] == values['plan_id']]
            result = {'tasks': [{k: v for k, v in t.items() if k != 'description'}
                                for t in rows], 'total_count': len(rows)}
        elif tool in ('create_plan', 'create_task'):
            if os.environ.get('PLANNING_UNCERTAIN_CREATE') == tool:
                save_planning_state()
                sys.exit('fixture uncertain create')
            rows = state['plans' if tool == 'create_plan' else 'tasks']
            result = dict(values, id=len(rows) + 1)
            if tool == 'create_plan':
                result.setdefault('status', 'draft')
            else:
                result.update(state='todo', version=1, assigned_agent=None)
            rows.append(result)
        elif tool in ('get_plan', 'get_task', 'update_plan', 'update_task'):
            kind = tool.split('_')[1]
            result = next(r for r in state[kind + 's'] if r['id'] == values[kind + '_id'])
            if tool.startswith('update'):
                result.update({k: v for k, v in values.items() if k != kind + '_id'})
        else:
            sys.exit('unsupported fixture call: ' + tool)
        save_planning_state()
        if os.environ.get('PLANNING_LOST_RESPONSE') == tool:
            sys.exit('fixture lost response')
        print(json.dumps(result))
        sys.exit(0)
'''
