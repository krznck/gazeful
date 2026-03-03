"""Integration tests for CSV data ingestion."""
import pytest
from debug import Samples, debug_time, ingest_sample


def test_ars_technica_sample():
    assert len(ingest_sample(Samples.ARS.value)) == 9353


def test_balatro_sample():
    assert len(ingest_sample(Samples.BALATRO.value)) == 47128


@pytest.mark.perf
def test_performance():
    for sample in Samples:
        debug_time(
            func=lambda: ingest_sample(sample.value),
            message=f"{sample.value} ingestion",
        )
