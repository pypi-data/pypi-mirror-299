import pytest

from ampdata.curves import TimeSeriesCurve
from ampdata.util import TS


@pytest.fixture
def ts1():
    points = [
        {"timestamp": 0, "value": 80},
        {"timestamp": 2678400000, "value": 90},
        {"timestamp": 5097600000, "value": 70},
        {"timestamp": 7776000000, "value": 120},
    ]
    return TS(
        id=1,
        name="This is a Name",
        frequency="M",
        time_zone="CET",
        curve_type=TimeSeriesCurve,
        points=points,
    )


@pytest.fixture
def ts2():
    points = [
        {"timestamp": 0, "value": 120},
        {"timestamp": 2678400000, "value": 210},
        {"timestamp": 5097600000, "value": 330},
        {"timestamp": 7776000000, "value": 380},
    ]
    return TS(
        id=2,
        name="This is another Name",
        frequency="M",
        time_zone="CET",
        curve_type=TimeSeriesCurve,
        points=points,
    )


@pytest.fixture
def ts3():
    points = [
        {"timestamp": 0, "value": 220},
        {"timestamp": 2678400000, "value": 120},
        {"timestamp": 5097600000, "value": 140},
        {"timestamp": 7776000000, "value": 580},
    ]
    return TS(
        id=3,
        name="This is a third Name",
        frequency="M",
        time_zone="CET",
        curve_type=TimeSeriesCurve,
        points=points,
    )


def test_to_pandas(ts1):
    pd_series = ts1.to_pandas()
    assert len(pd_series.index) == len(ts1.points)


def test_from_pandas(ts1):
    pd_series = ts1.to_pandas()
    re_ts = TS.from_pandas(pd_series)

    assert re_ts.name == ts1.name
    assert re_ts.frequency == ts1.frequency
    assert len(re_ts.points) == len(ts1.points)

    for dp1, dp2 in zip(re_ts.points, ts1.points):
        assert dp1 == dp2


def test_sum_ts(ts1, ts2, ts3):
    points = [
        {"timestamp": 0, "value": 420},
        {"timestamp": 2678400000, "value": 420},
        {"timestamp": 5097600000, "value": 540},
        {"timestamp": 7776000000, "value": 1080},
    ]
    sum_name = "Summed Series"
    summed = TS.sum([ts1, ts2, ts3], sum_name)

    assert summed.name == sum_name
    assert summed.frequency == ts1.frequency
    assert len(summed.points) >= len(ts1.points)
    assert len(summed.points) >= len(ts2.points)

    for dp1, dp2 in zip(points, summed.points):
        assert dp1 == dp2


def test_mean_ts(ts1, ts2, ts3):
    points = [
        {"timestamp": 0, "value": 140.0},
        {"timestamp": 2678400000, "value": 140},
        {"timestamp": 5097600000, "value": 180},
        {"timestamp": 7776000000, "value": 360},
    ]
    mean_name = "Mean Series"
    summed = TS.mean([ts1, ts2, ts3], mean_name)

    assert summed.name == mean_name
    assert summed.frequency == ts1.frequency
    assert len(summed.points) >= len(ts1.points)
    assert len(summed.points) >= len(ts2.points)

    for dp1, dp2 in zip(points, summed.points):
        assert dp1 == dp2


def test_median_ts(ts1, ts2, ts3):
    points = [
        {"timestamp": 0, "value": 120.0},
        {"timestamp": 2678400000, "value": 120},
        {"timestamp": 5097600000, "value": 140},
        {"timestamp": 7776000000, "value": 380},
    ]
    median_name = "Median Series"
    summed = TS.median([ts1, ts2, ts3], median_name)

    assert summed.name == median_name
    assert summed.frequency == ts1.frequency
    assert len(summed.points) >= len(ts1.points)
    assert len(summed.points) >= len(ts2.points)

    for dp1, dp2 in zip(points, summed.points):
        assert dp1 == dp2
