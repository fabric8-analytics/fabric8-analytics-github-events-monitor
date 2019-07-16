"""Tests for the monitor module."""

import json
import os

from unittest import mock

from ghmonitor import monitor
from ghmonitor.models import Event, EventType

GITHUB_GET_REPOS_RESPONSE = """
{
  "id": 724712,
  "node_id": "MDEwOlJlcG9zaXRvcnk3MjQ3MTI=",
  "name": "rust",
  "full_name": "rust-lang/rust",
  "private": false,
  "owner": {
    "login": "rust-lang",
    "id": 5430905,
    "node_id": "MDEyOk9yZ2FuaXphdGlvbjU0MzA5MDU=",
    "avatar_url": "https://avatars1.githubusercontent.com/u/5430905?v=4",
    "gravatar_id": "",
    "url": "https://api.github.com/users/rust-lang",
    "html_url": "https://github.com/rust-lang",
    "followers_url": "https://api.github.com/users/rust-lang/followers",
    "following_url": "https://api.github.com/users/rust-lang/following{/other_user}",
    "gists_url": "https://api.github.com/users/rust-lang/gists{/gist_id}",
    "starred_url": "https://api.github.com/users/rust-lang/starred{/owner}{/repo}",
    "subscriptions_url": "https://api.github.com/users/rust-lang/subscriptions",
    "organizations_url": "https://api.github.com/users/rust-lang/orgs",
    "repos_url": "https://api.github.com/users/rust-lang/repos",
    "events_url": "https://api.github.com/users/rust-lang/events{/privacy}",
    "received_events_url": "https://api.github.com/users/rust-lang/received_events",
    "type": "Organization",
    "site_admin": false
  },
  "html_url": "https://github.com/rust-lang/rust",
  "description": "Empowering everyone to build reliable and efficient software.",
  "fork": false,
  "url": "https://api.github.com/repos/rust-lang/rust",
  "forks_url": "https://api.github.com/repos/rust-lang/rust/forks",
  "keys_url": "https://api.github.com/repos/rust-lang/rust/keys{/key_id}",
  "collaborators_url": "https://api.github.com/repos/rust-lang/rust/collaborators{/collaborator}",
  "teams_url": "https://api.github.com/repos/rust-lang/rust/teams",
  "hooks_url": "https://api.github.com/repos/rust-lang/rust/hooks",
  "issue_events_url": "https://api.github.com/repos/rust-lang/rust/issues/events{/number}",
  "events_url": "https://api.github.com/repos/rust-lang/rust/events",
  "assignees_url": "https://api.github.com/repos/rust-lang/rust/assignees{/user}",
  "branches_url": "https://api.github.com/repos/rust-lang/rust/branches{/branch}",
  "tags_url": "https://api.github.com/repos/rust-lang/rust/tags",
  "blobs_url": "https://api.github.com/repos/rust-lang/rust/git/blobs{/sha}",
  "git_tags_url": "https://api.github.com/repos/rust-lang/rust/git/tags{/sha}",
  "git_refs_url": "https://api.github.com/repos/rust-lang/rust/git/refs{/sha}",
  "trees_url": "https://api.github.com/repos/rust-lang/rust/git/trees{/sha}",
  "statuses_url": "https://api.github.com/repos/rust-lang/rust/statuses/{sha}",
  "languages_url": "https://api.github.com/repos/rust-lang/rust/languages",
  "stargazers_url": "https://api.github.com/repos/rust-lang/rust/stargazers",
  "contributors_url": "https://api.github.com/repos/rust-lang/rust/contributors",
  "subscribers_url": "https://api.github.com/repos/rust-lang/rust/subscribers",
  "subscription_url": "https://api.github.com/repos/rust-lang/rust/subscription",
  "commits_url": "https://api.github.com/repos/rust-lang/rust/commits{/sha}",
  "git_commits_url": "https://api.github.com/repos/rust-lang/rust/git/commits{/sha}",
  "comments_url": "https://api.github.com/repos/rust-lang/rust/comments{/number}",
  "issue_comment_url": "https://api.github.com/repos/rust-lang/rust/issues/comments{/number}",
  "contents_url": "https://api.github.com/repos/rust-lang/rust/contents/{+path}",
  "compare_url": "https://api.github.com/repos/rust-lang/rust/compare/{base}...{head}",
  "merges_url": "https://api.github.com/repos/rust-lang/rust/merges",
  "archive_url": "https://api.github.com/repos/rust-lang/rust/{archive_format}{/ref}",
  "downloads_url": "https://api.github.com/repos/rust-lang/rust/downloads",
  "issues_url": "https://api.github.com/repos/rust-lang/rust/issues{/number}",
  "pulls_url": "https://api.github.com/repos/rust-lang/rust/pulls{/number}",
  "milestones_url": "https://api.github.com/repos/rust-lang/rust/milestones{/number}",
  "notifications_url":
  "https://api.github.com/repos/rust-lang/rust/notifications{?since,all,participating}",
  "labels_url": "https://api.github.com/repos/rust-lang/rust/labels{/name}",
  "releases_url": "https://api.github.com/repos/rust-lang/rust/releases{/id}",
  "deployments_url": "https://api.github.com/repos/rust-lang/rust/deployments",
  "created_at": "2010-06-16T20:39:03Z",
  "updated_at": "2019-01-03T11:01:45Z",
  "pushed_at": "2019-01-03T10:37:37Z",
  "git_url": "git://github.com/rust-lang/rust.git",
  "ssh_url": "git@github.com:rust-lang/rust.git",
  "clone_url": "https://github.com/rust-lang/rust.git",
  "svn_url": "https://github.com/rust-lang/rust",
  "homepage": "https://www.rust-lang.org",
  "size": 412185,
  "stargazers_count": 32869,
  "watchers_count": 32869,
  "language": "Rust",
  "has_issues": true,
  "has_projects": true,
  "has_downloads": true,
  "has_wiki": false,
  "has_pages": false,
  "forks_count": 5435,
  "mirror_url": null,
  "archived": false,
  "open_issues_count": 4768,
  "license": {
    "key": "other",
    "name": "Other",
    "spdx_id": "NOASSERTION",
    "url": null,
    "node_id": "MDc6TGljZW5zZTA="
  },
  "forks": 5435,
  "open_issues": 4768,
  "watchers": 32869,
  "default_branch": "master",
  "permissions": {
    "admin": false,
    "push": false,
    "pull": true
  },
  "organization": {
    "login": "rust-lang",
    "id": 5430905,
    "node_id": "MDEyOk9yZ2FuaXphdGlvbjU0MzA5MDU=",
    "avatar_url": "https://avatars1.githubusercontent.com/u/5430905?v=4",
    "gravatar_id": "",
    "url": "https://api.github.com/users/rust-lang",
    "html_url": "https://github.com/rust-lang",
    "followers_url": "https://api.github.com/users/rust-lang/followers",
    "following_url": "https://api.github.com/users/rust-lang/following{/other_user}",
    "gists_url": "https://api.github.com/users/rust-lang/gists{/gist_id}",
    "starred_url": "https://api.github.com/users/rust-lang/starred{/owner}{/repo}",
    "subscriptions_url": "https://api.github.com/users/rust-lang/subscriptions",
    "organizations_url": "https://api.github.com/users/rust-lang/orgs",
    "repos_url": "https://api.github.com/users/rust-lang/repos",
    "events_url": "https://api.github.com/users/rust-lang/events{/privacy}",
    "received_events_url": "https://api.github.com/users/rust-lang/received_events",
    "type": "Organization",
    "site_admin": false
  },
  "network_count": 5435,
  "subscribers_count": 1369
}
"""

GITHUB_GET_REPOS_RESPONSE_KUBERNETES = """
{
  "id": 82102742,
  "node_id": "MDEwOlJlcG9zaXRvcnk4MjEwMjc0Mg==",
  "name": "metrics",
  "full_name": "kubernetes/metrics",
  "private": false,
  "owner": {
    "login": "kubernetes",
    "id": 13629408,
    "node_id": "MDEyOk9yZ2FuaXphdGlvbjEzNjI5NDA4",
    "avatar_url": "https://avatars2.githubusercontent.com/u/13629408?v=4",
    "gravatar_id": "",
    "url": "https://api.github.com/users/kubernetes",
    "html_url": "https://github.com/kubernetes",
    "followers_url": "https://api.github.com/users/kubernetes/followers",
    "following_url": "https://api.github.com/users/kubernetes/following{/other_user}",
    "gists_url": "https://api.github.com/users/kubernetes/gists{/gist_id}",
    "starred_url": "https://api.github.com/users/kubernetes/starred{/owner}{/repo}",
    "subscriptions_url": "https://api.github.com/users/kubernetes/subscriptions",
    "organizations_url": "https://api.github.com/users/kubernetes/orgs",
    "repos_url": "https://api.github.com/users/kubernetes/repos",
    "events_url": "https://api.github.com/users/kubernetes/events{/privacy}",
    "received_events_url": "https://api.github.com/users/kubernetes/received_events",
    "type": "Organization",
    "site_admin": false
  },
  "html_url": "https://github.com/kubernetes/metrics",
  "description": "Kubernetes metrics-related API types and clients",
  "fork": false,
  "url": "https://api.github.com/repos/kubernetes/metrics",
  "forks_url": "https://api.github.com/repos/kubernetes/metrics/forks",
  "keys_url": "https://api.github.com/repos/kubernetes/metrics/keys{/key_id}",
  "collaborators_url":
  "https://api.github.com/repos/kubernetes/metrics/collaborators{/collaborator}",
  "teams_url": "https://api.github.com/repos/kubernetes/metrics/teams",
  "hooks_url": "https://api.github.com/repos/kubernetes/metrics/hooks",
  "issue_events_url": "https://api.github.com/repos/kubernetes/metrics/issues/events{/number}",
  "events_url": "https://api.github.com/repos/kubernetes/metrics/events",
  "assignees_url": "https://api.github.com/repos/kubernetes/metrics/assignees{/user}",
  "branches_url": "https://api.github.com/repos/kubernetes/metrics/branches{/branch}",
  "tags_url": "https://api.github.com/repos/kubernetes/metrics/tags",
  "blobs_url": "https://api.github.com/repos/kubernetes/metrics/git/blobs{/sha}",
  "git_tags_url": "https://api.github.com/repos/kubernetes/metrics/git/tags{/sha}",
  "git_refs_url": "https://api.github.com/repos/kubernetes/metrics/git/refs{/sha}",
  "trees_url": "https://api.github.com/repos/kubernetes/metrics/git/trees{/sha}",
  "statuses_url": "https://api.github.com/repos/kubernetes/metrics/statuses/{sha}",
  "languages_url": "https://api.github.com/repos/kubernetes/metrics/languages",
  "stargazers_url": "https://api.github.com/repos/kubernetes/metrics/stargazers",
  "contributors_url": "https://api.github.com/repos/kubernetes/metrics/contributors",
  "subscribers_url": "https://api.github.com/repos/kubernetes/metrics/subscribers",
  "subscription_url": "https://api.github.com/repos/kubernetes/metrics/subscription",
  "commits_url": "https://api.github.com/repos/kubernetes/metrics/commits{/sha}",
  "git_commits_url": "https://api.github.com/repos/kubernetes/metrics/git/commits{/sha}",
  "comments_url": "https://api.github.com/repos/kubernetes/metrics/comments{/number}",
  "issue_comment_url": "https://api.github.com/repos/kubernetes/metrics/issues/comments{/number}",
  "contents_url": "https://api.github.com/repos/kubernetes/metrics/contents/{+path}",
  "compare_url": "https://api.github.com/repos/kubernetes/metrics/compare/{base}...{head}",
  "merges_url": "https://api.github.com/repos/kubernetes/metrics/merges",
  "archive_url": "https://api.github.com/repos/kubernetes/metrics/{archive_format}{/ref}",
  "downloads_url": "https://api.github.com/repos/kubernetes/metrics/downloads",
  "issues_url": "https://api.github.com/repos/kubernetes/metrics/issues{/number}",
  "pulls_url": "https://api.github.com/repos/kubernetes/metrics/pulls{/number}",
  "milestones_url": "https://api.github.com/repos/kubernetes/metrics/milestones{/number}",
  "notifications_url":
  "https://api.github.com/repos/kubernetes/metrics/notifications{?since,all,participating}",
  "labels_url": "https://api.github.com/repos/kubernetes/metrics/labels{/name}",
  "releases_url": "https://api.github.com/repos/kubernetes/metrics/releases{/id}",
  "deployments_url": "https://api.github.com/repos/kubernetes/metrics/deployments",
  "created_at": "2017-02-15T20:21:09Z",
  "updated_at": "2018-12-24T02:37:57Z",
  "pushed_at": "2018-12-21T20:51:34Z",
  "git_url": "git://github.com/kubernetes/metrics.git",
  "ssh_url": "git@github.com:kubernetes/metrics.git",
  "clone_url": "https://github.com/kubernetes/metrics.git",
  "svn_url": "https://github.com/kubernetes/metrics",
  "homepage": "",
  "size": 4532,
  "stargazers_count": 138,
  "watchers_count": 138,
  "language": "Go",
  "has_issues": true,
  "has_projects": true,
  "has_downloads": true,
  "has_wiki": true,
  "has_pages": false,
  "forks_count": 46,
  "mirror_url": null,
  "archived": false,
  "open_issues_count": 0,
  "license": {
    "key": "apache-2.0",
    "name": "Apache License 2.0",
    "spdx_id": "Apache-2.0",
    "url": "https://api.github.com/licenses/apache-2.0",
    "node_id": "MDc6TGljZW5zZTI="
  },
  "forks": 46,
  "open_issues": 0,
  "watchers": 138,
  "default_branch": "master",
  "permissions": {
    "admin": false,
    "push": false,
    "pull": true
  },
  "organization": {
    "login": "kubernetes",
    "id": 13629408,
    "node_id": "MDEyOk9yZ2FuaXphdGlvbjEzNjI5NDA4",
    "avatar_url": "https://avatars2.githubusercontent.com/u/13629408?v=4",
    "gravatar_id": "",
    "url": "https://api.github.com/users/kubernetes",
    "html_url": "https://github.com/kubernetes",
    "followers_url": "https://api.github.com/users/kubernetes/followers",
    "following_url": "https://api.github.com/users/kubernetes/following{/other_user}",
    "gists_url": "https://api.github.com/users/kubernetes/gists{/gist_id}",
    "starred_url": "https://api.github.com/users/kubernetes/starred{/owner}{/repo}",
    "subscriptions_url": "https://api.github.com/users/kubernetes/subscriptions",
    "organizations_url": "https://api.github.com/users/kubernetes/orgs",
    "repos_url": "https://api.github.com/users/kubernetes/repos",
    "events_url": "https://api.github.com/users/kubernetes/events{/privacy}",
    "received_events_url": "https://api.github.com/users/kubernetes/received_events",
    "type": "Organization",
    "site_admin": false
  },
  "network_count": 46,
  "subscribers_count": 26
}
"""

GITHUB_GET_REPOS_RESPONSE_NOT_FOUND = """{
  "message": "Not Found",
  "documentation_url": "https://developer.github.com/v3/repos/#get"
}"""


def mocked_github_request(url, **_kwargs):
    """Return predefined response."""
    if url.startswith('https://api.github.com/'):
        if '/repos/' in url and '/rust-lang/rust' in url:
            return 200, json.loads(GITHUB_GET_REPOS_RESPONSE)
        elif '/repos/' in url and '/kubernetes/metrics' in url:
            return 200, json.loads(GITHUB_GET_REPOS_RESPONSE_KUBERNETES)
        elif '/issues/' in url:
            pass
        elif '/pulls/' in url:
            pass
        else:
            return 404, json.loads(GITHUB_GET_REPOS_RESPONSE_NOT_FOUND)
    else:
        return None


@mock.patch('ghmonitor.monitor.github_request', side_effect=mocked_github_request)
def test_repository_exists(github_request_function):
    """Test it."""
    assert github_request_function is not None
    assert monitor.repository_exists('rust-lang/rust') is True
    assert monitor.repository_exists('msehnout/go-lang-is-awesome') is False


def test_get_auth_header():
    """Test it."""
    os.environ['GITHUB_TOKEN'] = '123'
    assert monitor.get_auth_header() == {'Authorization': 'token 123'}
    os.environ.pop('GITHUB_TOKEN')
    assert monitor.get_auth_header() is None


def test_get_list_of_repos():
    """Test it."""
    os.environ['WATCH_REPOS'] = 'a/b c/d'
    assert monitor.get_list_of_repos() == ['a/b', 'c/d']


def test_get_list_of_packages():
    """Test it."""
    os.environ['WATCH_PACKAGES'] = 'a/b c/d'
    assert monitor.get_list_of_repos() == ['a/b', 'c/d']


def test_github_request():
    """Test it."""
    assert monitor.github_request('https://api.github.com/') is not None
    assert monitor.github_request('https://tramtadadaneexistujicidomena.redhat.com/') is None
    assert monitor.github_request('https://github.com/') is None


def test_new_issues():
    """Test set operations."""
    m = monitor.RepositoryMonitor('a', 'b')
    i1 = Event()
    i1.type = EventType.ISSUE
    i2 = Event()
    i2.id = 1
    i2.type = EventType.ISSUE
    c1 = Event()
    c1.type = EventType.PUSH
    c2 = Event()
    c2.id = 1
    c2.type = EventType.PUSH
    p1 = Event()
    p1.type = EventType.PULL_REQUEST
    p2 = Event()
    p2.id = 1
    p2.type = EventType.PULL_REQUEST
    m.seen_events = set()
    new_events = set()
    assert m.new_commits(new_events) == set()
    assert m.new_issues(new_events) == set()
    assert m.new_pull_requests(new_events) == set()
    m.seen_events = {i1, c1, p1}
    new_events = {i1, c1, p1}
    assert m.new_commits(new_events) == set()
    assert m.new_issues(new_events) == set()
    assert m.new_pull_requests(new_events) == set()
    m.seen_events = {i1, c1, p1}
    new_events = {i1, c1, p1, i2, c2, p2}
    assert m.new_commits(new_events)
    assert m.new_issues(new_events)
    assert m.new_pull_requests(new_events)
