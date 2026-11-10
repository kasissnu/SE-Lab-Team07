"""Branch-coverage tests for ski_resort_pass."""

import pytest

from CodeCoverageTest_08_ski_resort_pass import group, skier
from ski_resort_pass import check_chairlift_anemometer, process_resort_bookings


def test_input_and_group_decisions():
    with pytest.raises(ValueError):
        process_resort_bookings({}, 10)
    with pytest.raises(ValueError):
        process_resort_bookings([], -0.01)
    assert process_resort_bookings([group(active=False)], 10)["status"] == "ZERO_SALES"
    assert process_resort_bookings([group("unknown")], 10)["status"] == "ZERO_SALES"


def test_all_duration_branches():
    groups = [
        group("season", skiers=[skier(30)]),
        group("full_day", skiers=[skier(30)]),
        group("half_day", skiers=[skier(30)]),
    ]
    assert process_resort_bookings(groups, 0)["total_revenue"] == 430.0


def test_age_blackout_rental_and_locker_branches():
    groups = [
        group(
            "full_day",
            skiers=[
                skier(0),
                skier(11),
                skier(65),
                skier(30, gear_rental=True),
                skier(30, blackout_override=True),
            ],
            locker=True,
        ),
        group(
            "half_day",
            skiers=[skier(30, blackout_override=True), skier(30)],
        ),
    ]
    result = process_resort_bookings(groups, 15)
    assert result["status"] == "COMPLETED"
    assert result["total_revenue"] == 274.0


def test_audit_review_and_zero_sales_returns():
    rejected = [group("invalid") for _ in range(5)]
    assert process_resort_bookings(rejected, 10)["status"] == "AUDIT_REVIEW"
    assert process_resort_bookings([group("half_day", skiers=[skier(0)])], 10) == {
        "total_revenue": 0.0,
        "status": "ZERO_SALES",
    }


def test_anemometer_branches():
    assert check_chairlift_anemometer(None) == "NO_DATA"
    assert check_chairlift_anemometer([[46, 20, 47, 20]]) == "SAFE_OPERATION"
    assert check_chairlift_anemometer([[45, 46, 47]]) == "SUSPEND_LIFT"
