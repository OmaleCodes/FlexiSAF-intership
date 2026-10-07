import pytest

from src.decorators import retry, timed


def test_timed_returns_same_result():
    @timed
    def add(a: int, b: int) -> int:
        return a + b

    assert add(2, 3) == 5


def test_retry_succeeds_eventually():
    calls = {"count": 0}

    @retry(times=3, delay=0)
    def flaky() -> str:
        calls["count"] += 1
        if calls["count"] < 3:
            raise ValueError("fail")
        return "ok"

    assert flaky() == "ok"
    assert calls["count"] == 3


def test_retry_raises_after_exhausting_attempts():
    @retry(times=2, delay=0)
    def always_fails() -> None:
        raise ValueError("fail")

    with pytest.raises(ValueError):
        always_fails()


def test_retry_does_not_retry_on_first_success():
    calls = {"count": 0}

    @retry(times=3, delay=0)
    def succeeds_immediately() -> str:
        calls["count"] += 1
        return "ok"

    assert succeeds_immediately() == "ok"
    assert calls["count"] == 1