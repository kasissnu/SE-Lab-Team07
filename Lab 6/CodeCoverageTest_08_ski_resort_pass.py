"""Line-coverage tests for ski_resort_pass."""

import pytest

from ski_resort_pass import check_chairlift_anemometer, process_resort_bookings


def skier(age, gear_rental=False, blackout_override=False):
    return {
        "age": age,
        "gear_rental": gear_rental,
        "blackout_override": blackout_override,
    }


def group(duration="full_day", active=True, skiers=None, locker=False):
    return {
        "is_active": active,
        "duration": duration,
        "skiers": [] if skiers is None else skiers,
        "includes_lodge_locker": locker,
    }


def test_rejects_invalid_arguments_and_skips_inactive_groups():
    with pytest.raises(ValueError):
        process_resort_bookings("not a list", 10)
    with pytest.raises(ValueError):
        process_resort_bookings([], -1)
    result = process_resort_bookings([group(active=False)], 10)
    assert result == {"total_revenue": 0.0, "status": "ZERO_SALES"}


def test_prices_every_duration_and_age_category():
    groups = [
        group("season", skiers=[skier(30)]),
        group("full_day", skiers=[skier(11)]),
        group("half_day", skiers=[skier(65)]),
        group("full_day", skiers=[skier(30)]),
    ]
    result = process_resort_bookings(groups, 15)
    assert result == {"total_revenue": 463.0, "status": "COMPLETED"}


def test_adds_gear_and_locker_fees():
    result = process_resort_bookings(
        [group(skiers=[skier(30, gear_rental=True)], locker=True)], 20
    )
    assert result == {"total_revenue": 135.0, "status": "COMPLETED"}


def test_handles_invalid_age_and_blackout_rules():
    groups = [
        group("full_day", skiers=[skier(0)]),
        group("full_day", skiers=[skier(30, blackout_override=True)]),
        group("half_day", skiers=[skier(30, blackout_override=True), skier(30)]),
    ]
    result = process_resort_bookings(groups, 10)
    assert result == {"total_revenue": 40.0, "status": "COMPLETED"}


def test_rejects_unknown_duration_and_escalates_many_rejections():
    groups = [group("hourly") for _ in range(5)]
    result = process_resort_bookings(groups, 10)
    assert result == {"total_revenue": 0.0, "status": "AUDIT_REVIEW"}


def test_anemometer_reports_all_operating_states():
    assert check_chairlift_anemometer([]) == "NO_DATA"
    assert check_chairlift_anemometer([[45, 20, 46, 20]]) == "SAFE_OPERATION"
    assert check_chairlift_anemometer([[46, 47]]) == "SUSPEND_LIFT"


def test_anemometer_accepts_multiple_lifts():
    assert check_chairlift_anemometer([[20], [30, 45]]) == "SAFE_OPERATION"
