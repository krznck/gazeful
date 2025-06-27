from debug import debug_time
from debug import ingest_sample


def test_ars_technica_sample():
    stream = debug_time(lambda: ingest_sample("ars_technica"), "ars sample ingestion")

    assert len(stream) == 9353


def test_balatro_sample():
    stream = debug_time(lambda: ingest_sample("balatro"), "balatro sample ingestion")

    assert len(stream) == 47128
