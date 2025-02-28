
import datetime
from typing import Tuple

import pytest

from dharitrietl.indexer import Indexer


@pytest.mark.integration
def test_count_records():
    start_timestamp, end_timestamp = _make_recent_time_slice(24 * 60 * 60)

    indexer = Indexer("https://index.dharitri.org")
    count = indexer.count_records("transactions", start_timestamp, end_timestamp)
    assert count > 42

    indexer = Indexer("https://devnet-index.dharitri.org")
    count = indexer.count_records("transactions", start_timestamp, end_timestamp)
    assert count > 0

    indexer = Indexer("https://testnet-index.dharitri.org")
    count = indexer.count_records("transactions", start_timestamp, end_timestamp)
    assert count > 0


@pytest.mark.integration
def test_get_records():
    indexer = Indexer("https://index.dharitri.org")
    records = indexer.get_records("transactions", *_make_recent_time_slice(60))
    assert any(records)

    indexer = Indexer("https://devnet-index.dharitri.org")
    records = indexer.get_records("transactions", *_make_recent_time_slice(60 * 60))
    assert any(records)

    indexer = Indexer("https://testnet-index.dharitri.org")
    records = indexer.get_records("transactions", *_make_recent_time_slice(24 * 60 * 60))
    assert any(records)


def _make_recent_time_slice(duration_in_seconds: int) -> Tuple[int, int]:
    now = datetime.datetime.now(tz=datetime.timezone.utc)
    now_timestamp = int(now.timestamp())
    some_time_ago = (now - datetime.timedelta(seconds=duration_in_seconds))
    some_time_ago_timestamp = int(some_time_ago.timestamp())
    return some_time_ago_timestamp, now_timestamp
