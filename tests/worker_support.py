"""Local worker setup choices; controlled native processes only."""


def worker_settings(fixture, *, harness='codex', model='gpt-5.4', effort='xhigh'):
    tdd = fixture.workspace / 'tdd/SKILL.md'
    tdd.parent.mkdir(exist_ok=True)
    tdd.write_text('---\nname: tdd\ndescription: Sequential TDD.\n---\nTest first.\n')
    standard = fixture.workspace / 'standards/SKILL.md'
    standard.parent.mkdir(exist_ok=True)
    standard.write_text('---\nname: standards\ndescription: Coding standards.\n'
                        '---\nKeep it simple.\n')
    for command in ('codex', 'claude'):
        path = fixture.bin / command
        path.write_text(CATALOG)
        path.chmod(0o755)
    return ('--implementation-model', model, '--implementation-harness', harness,
            '--implementation-effort', effort, '--review-model', 'opus',
            '--review-harness', 'claude_code', '--review-effort', 'high',
            '--tdd-skill', str(tdd), '--implementation-skill', str(standard),
            '--review-skill', str(standard))


CATALOG = r'''#!/usr/bin/env python3
import json
import os
import sys
from pathlib import Path
if os.environ.get('WORKER_CATALOG_LOG'):
    with open(os.environ['WORKER_CATALOG_LOG'], 'a') as stream:
        stream.write(json.dumps({'harness': Path(sys.argv[0]).name, 'cwd': os.getcwd()}) + '\n')
if os.environ.get('WORKER_CATALOG_FAIL'):
    raise SystemExit('TOP_SECRET native catalog failed')
if Path(sys.argv[0]).name == 'codex' and sys.argv[1:] == ['debug', 'models']:
    print(json.dumps({'models': [{'slug': value, 'visibility': 'list'}
                                  for value in json.loads(os.environ.get(
                                      'WORKER_CODEX_MODELS', '["gpt-5.4"]'))]}))
elif Path(sys.argv[0]).name == 'claude' and '--input-format' in sys.argv:
    request = json.loads(sys.stdin.readline())
    assert request['request']['subtype'] == 'initialize'
    print(json.dumps({'type': 'control_response', 'response': {
        'request_id': request['request_id'], 'subtype': 'success',
        'response': {'models': [{'value': 'opus'}]}}}))
else:
    raise SystemExit('Unexpected native worker launch')
'''
