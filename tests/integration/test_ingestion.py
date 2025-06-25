from debug import ingest_sample


def test_ars_technica_sample():
    points = ingest_sample("ars_technica")

    assert len(points) == 9353


def test_balatro_sample():
    points = ingest_sample("balatro")

    assert len(points) == 47128
