"""Test the awesome models."""

from ghmonitor.models import Event, UnknownEvent, EventType


def test_event_types_from_str():
    """Test conversion str->type."""
    assert EventType.PUSH == EventType.from_str("PushEvent")
    assert EventType.ISSUE == EventType.from_str("IssuesEvent")
    assert EventType.PULL_REQUEST == EventType.from_str("PullRequestEvent")
    try:
        EventType.from_str("foobar")
    except Exception as e:
        assert isinstance(e, UnknownEvent)


def test_event_parser_returns_event():
    """Test the constructor."""
    print("Testing data parser")
    a = {"id": "222", "type": "PushEvent", "repo": {"name": "a"}}
    b = {"id": "222", "tpe": "PushEvent", "repo": {"name": "a"}}
    assert isinstance(Event.from_dict(a), Event)
    assert Event.from_dict(b) is None


def test_events_comparison():
    """Test eq operator."""
    e0 = Event()
    e1 = Event()
    assert e0 == e1
    e0.repo = 'a'
    assert not(e0 == e1)
    e1.repo = 'a'
    e0.id = 1
    e1.id = 1
    e0.type = EventType.PUSH
    e1.type = EventType.PUSH
    assert e0 == e1


def test_event_from_non_valid_json():
    """Test conversion failures."""
    a = Event.from_dict({"id": "foo", "type": "PushEvent", "repo": {"name": "a"}})
    assert a is None
    a = Event.from_dict({"id": "222", "type": "FooEvent", "repo": {"name": "a"}})
    assert a is None
    a = Event.from_dict({"id": "222", "type": "PushEvent", "repo": ""})
    assert a is None
    a = Event.from_dict({"foo": "bar"})
    assert a is None
    a = Event.from_dict({"foo": "bar", "type": "11111555666666666661111155566666666666"})
    assert a is None
