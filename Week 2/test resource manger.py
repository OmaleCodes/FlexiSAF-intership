import pytest

from src.resource_manager import managed_resource


def test_resource_opens_and_closes():
    with managed_resource("test") as resource:
        assert resource.is_open is True
        assert resource.use() == "using test"
    assert resource.is_open is False


def test_resource_closes_even_on_exception():
    captured = {}
    with pytest.raises(ValueError), managed_resource("test") as resource:
        captured["resource"] = resource
        raise ValueError("boom")
    assert captured["resource"].is_open is False


def test_use_before_open_raises():
    from src.resource_manager import ManagedResource

    resource = ManagedResource("unopened")
    with pytest.raises(RuntimeError):
        resource.use()