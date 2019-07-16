"""Test utils file."""

import json
import os

from unittest import mock

from ghmonitor.backend import Backend
from ghmonitor.models import Event, EventType
from ghmonitor.monitor import RepositoryMonitor
from ghmonitor.utils import create_monitors, process_new_events
from tests.test_monitor import mocked_github_request

# NOTE: Not necessary, the real request should work every time
# GO_GET_RESPONSE = """
#
# <html><head>
#       <meta name="go-import"
#             content="k8s.io/metrics
#                      git https://github.com/kubernetes/metrics">
#       <meta name="go-source"
#             content="k8s.io/metrics
#                      https://github.com/kubernetes/metrics
#                      https://github.com/kubernetes/metrics/tree/master{/dir}
#                      https://github.com/kubernetes/metrics/blob/master{/dir}/{file}#L{line}">
# </head></html>
# """


@mock.patch('ghmonitor.monitor.github_request', side_effect=mocked_github_request)
def test_create_monitors(github_request_function):
    """Test create monitors function."""
    os.environ['WATCH_PACKAGES'] = 'k8s.io/metrics'
    monitors = create_monitors()
    m = monitors[0]
    assert github_request_function is not None
    assert m.name == 'kubernetes/metrics'
    assert m.package == 'k8s.io/metrics'


class MockBackend(Backend):
    """Just a testing backend."""

    def __init__(self):
        """Construct it."""
        self.notifications = []

    def notify(self, notification_string):
        """Store notifications in a list."""
        self.notifications += [notification_string]


def mocked_get_new_events():
    """Create dummy events."""
    i1 = Event()
    i1.type = EventType.ISSUE
    i1.id = 5

    i2 = Event()
    i2.type = EventType.PULL_REQUEST
    i2.id = 6

    i3 = Event()
    i3.type = EventType.PUSH

    return {i1, i2, i3}


EXPECTED_ISSUE_NOTIFICATION = """
{
        "repository": "kubernetes/metrics",
        "package": "k8s.io/metrics",
        "event": "issue",
        "id": 5
}
"""

EXPECTED_PR_NOTIFICATION = """
{
        "repository": "kubernetes/metrics",
        "package": "k8s.io/metrics",
        "event": "pull-request",
        "id": 6
}
"""

EXPECTED_PUSH_NOTIFICATION = """
{
        "repository": "kubernetes/metrics",
        "package": "k8s.io/metrics",
        "event": "push"
}
"""


@mock.patch('ghmonitor.monitor.RepositoryMonitor.get_new_events', side_effect=mocked_get_new_events)
def test_process_new_events(get_new_events):
    """Test it all! Use all the prepared data from above."""
    assert get_new_events is not None

    monitor = RepositoryMonitor('k8s.io/metrics', 'kubernetes/metrics')
    monitor.seen_events = set()
    backend = MockBackend()
    process_new_events(monitor, backend)
    # There are new notifications
    assert len(backend.notifications) > 0

    # Issue notification
    issue_notification = json.loads(backend.notifications[0])
    expected_notification = json.loads(EXPECTED_ISSUE_NOTIFICATION)
    assert issue_notification == expected_notification

    # Push notification
    push_notification = json.loads(backend.notifications[1])
    expected_notification = json.loads(EXPECTED_PUSH_NOTIFICATION)
    assert push_notification == expected_notification

    # PR notification
    pr_notification = json.loads(backend.notifications[2])
    expected_notification = json.loads(EXPECTED_PR_NOTIFICATION)
    assert pr_notification == expected_notification
