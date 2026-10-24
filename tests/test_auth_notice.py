"""Authentication guidance through public init and a disposable HTTP policy endpoint."""
import json
import threading
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer

from test_init import INIT_SETTINGS, InitFixture


class AuthNoticeTests(InitFixture):
    def setUp(self):
        super().setUp()
        self.policy = {'authEnabled': False, 'authMode': 'disabled'}
        self.status = 200
        self.requests = []
        self.hold_response = False
        self.release = threading.Event()
        fixture = self

        class Handler(BaseHTTPRequestHandler):
            def do_GET(self):
                fixture.requests.append((self.path, dict(self.headers)))
                data = (fixture.policy if isinstance(fixture.policy, bytes)
                        else json.dumps(fixture.policy).encode())
                self.send_response(fixture.status)
                self.send_header('Content-Type', 'application/json')
                self.send_header('Content-Length', str(len(data)))
                if fixture.status == 302:
                    self.send_header('Location', '/do-not-follow')
                self.end_headers()
                if fixture.hold_response:
                    fixture.release.wait(5)
                try:
                    self.wfile.write(data)
                except OSError:
                    pass

            def log_message(self, *_args):
                pass

        server = ThreadingHTTPServer(('127.0.0.1', 0), Handler)
        worker = threading.Thread(target=server.serve_forever, kwargs={'poll_interval': 0.02})
        worker.start()
        self.addCleanup(worker.join)
        self.addCleanup(server.server_close)
        self.addCleanup(server.shutdown)
        self.addCleanup(self.release.set)
        self.server = f'http://127.0.0.1:{server.server_port}'

    def setup_server(self, repo, path='/mcp'):
        return self.run_cli(repo, '--repo', '.', *INIT_SETTINGS,
                            '--forgetful-instance', 'server',
                            '--forgetful-server', self.server + path)

    def test_disabled_auth_has_no_browser_notice(self):
        # Arrange
        repo = self.repo()
        # Act
        result = self.setup_server(repo)
        # Assert
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertNotIn('If your browser opens', result.stdout)
        self.assertEqual([path for path, _ in self.requests], ['/api/v1/auth/info'])

    def test_oauth_notice_uses_public_policy_under_the_server_prefix(self):
        # Arrange
        repo = self.repo()
        self.policy = {'authEnabled': True, 'authMode': 'oauth',
                       'loginUrl': 'https://not-a-login-to-follow.example'}
        # Act
        result = self.setup_server(repo, '/forgetful/mcp')
        # Assert
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn('If your browser opens, complete Forgetful sign-in there.', result.stdout)
        self.assertEqual([path for path, _ in self.requests], ['/forgetful/api/v1/auth/info'])
        headers = {key.lower(): value for key, value in self.requests[0][1].items()}
        self.assertNotIn('authorization', headers)
        self.assertNotIn('cookie', headers)

    def test_non_browser_modes_and_unknown_policy_do_not_suggest_login(self):
        for index, (status, policy) in enumerate([
            (200, {'authEnabled': True, 'authMode': 'jwt'}),
            (200, {'authEnabled': True, 'authMode': 'introspection'}),
            (200, {'authEnabled': 'true', 'authMode': 'oauth'}),
            (200, {'authEnabled': False, 'authMode': 'oauth'}),
            (200, {'authEnabled': True, 'authMode': 'future-mode'}),
            (200, []), (200, b'invalid json'),
            (200, b'[' * 4000 + b'0' + b']' * 4000),
            (404, {}), (503, {}),
            (302, {'authEnabled': True, 'authMode': 'oauth'}),
            (200, {'authEnabled': True, 'authMode': 'oauth', 'extra': 'x' * 9000}),
        ]):
            with self.subTest(status=status, policy_type=type(policy).__name__, index=index):
                # Arrange
                repo = self.repo(f'app-{index}')
                self.status, self.policy = status, policy
                self.requests.clear()
                # Act
                result = self.setup_server(repo)
                # Assert
                self.assertEqual(result.returncode, 0, result.stderr)
                self.assertNotIn('If your browser opens', result.stdout)
                self.assertEqual([path for path, _ in self.requests], ['/api/v1/auth/info'])
                self.assertTrue((repo / '.factory/setup-complete.json').exists())

    def test_policy_timeout_does_not_skip_the_real_access_check(self):
        # Arrange
        repo = self.repo()
        self.policy = {'authEnabled': True, 'authMode': 'oauth'}
        self.hold_response = True
        self.env['PROFILE_FAIL'] = 'forgetful'
        # Act
        result = self.setup_server(repo)
        # Assert
        self.assertNotEqual(result.returncode, 0)
        self.assertIn('Forgetful planning check failed', result.stderr)
        self.assertNotIn('If your browser opens', result.stdout)
        self.assertFalse((repo / '.factory/setup-complete.json').exists())

    def test_local_setup_does_not_request_server_policy(self):
        # Arrange
        repo = self.repo()
        # Act
        result = self.run_cli(repo, '--repo', '.', *INIT_SETTINGS)
        # Assert
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertNotIn('If your browser opens', result.stdout)
        self.assertEqual(self.requests, [])
