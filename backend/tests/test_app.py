
import unittest
import sys
from pathlib import Path

# Make the backend folder accessible to Python
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from app import app


class TestAIDevOpsAssistant(unittest.TestCase):

    def setUp(self):
        self.client = app.test_client()

    # Test 1: Health check
    def test_health_check(self):
        response = self.client.get('/api/health')

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json['status'], 'success')

    # Test 2: Docker port conflict
    def test_docker_port_conflict(self):
        response = self.client.post('/api/analyze', json={
            'logType': 'docker',
            'logContent': 'Error: port is already allocated'
        })

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json['analysis']['error'], 'Port Conflict')
        self.assertEqual(response.json['analysis']['severity'], 'High')

    # Test 3: Linux permission denied
    def test_linux_permission_denied(self):
        response = self.client.post('/api/analyze', json={
            'logType': 'linux',
            'logContent': 'Permission denied'
        })

        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            response.json['analysis']['error'],
            'Permission Denied'
        )

    # Test 4: Linux missing file
    def test_linux_file_not_found(self):
        response = self.client.post('/api/analyze', json={
            'logType': 'linux',
            'logContent': 'No such file or directory'
        })

        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            response.json['analysis']['error'],
            'File or Directory Not Found'
        )

    # Test 5: Linux connection refused
    def test_linux_connection_refused(self):
        response = self.client.post('/api/analyze', json={
            'logType': 'linux',
            'logContent': 'Connection refused'
        })

        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            response.json['analysis']['error'],
            'Connection Refused'
        )

    # Test 6: Jenkins build failure
    def test_jenkins_build_failure(self):
        response = self.client.post('/api/analyze', json={
            'logType': 'jenkins',
            'logContent': 'Finished: FAILURE'
        })

        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            response.json['analysis']['error'],
            'Jenkins Build Failure'
        )
        self.assertEqual(response.json['analysis']['severity'], 'High')

    # Test 7: Invalid log type
    def test_invalid_log_type(self):
        response = self.client.post('/api/analyze', json={
            'logType': 'unknown',
            'logContent': 'Some error'
        })

        self.assertEqual(response.status_code, 400)

    # Test 8: Empty log content
    def test_empty_log_content(self):
        response = self.client.post('/api/analyze', json={
            'logType': 'linux',
            'logContent': ''
        })

        self.assertEqual(response.status_code, 400)


if __name__ == '__main__':
    unittest.main()
