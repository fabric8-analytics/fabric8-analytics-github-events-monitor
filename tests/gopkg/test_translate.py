"""Test the gopkg module."""

from ghmonitor.gopkg.translate import get_repo_from_random_urn, translate, GITHUB_REPO_RE


def test_get_repo_urn():
    """Test the function. Be careful though, it requires an Internet access."""
    assert 'kubernetes/metrics' == get_repo_from_random_urn('k8s.io/metrics')
    assert get_repo_from_random_urn('seznam.cz') is None


def test_github_re():
    """Test the regular expression."""
    assert GITHUB_REPO_RE.match('bitbucket.com/user/repo') is None
    m = GITHUB_REPO_RE.match('github.com/user/project')
    assert m.group('user') == 'user'
    assert m.group('repo') == 'project'
    m = GITHUB_REPO_RE.match('github.com/user/project/folder')
    assert m.group('user') == 'user'
    assert m.group('repo') == 'project'


def test_translate():
    """Test the translation. Again, needs Internet access."""
    assert 'kubernetes/metrics' == translate('k8s.io/metrics')
    assert 'user/project' == translate('github.com/user/project')
    assert translate('launchpad.net/project') is None
