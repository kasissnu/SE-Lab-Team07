from hypothesis import given, strategies as st

from processor import (
    calculate_lift_access_tier,
    compute_trail_gradient,
    parse_season_pass_validity,
)


@given(st.one_of(st.text(), st.none()))
def test_parse_season_pass_validity_no_crash(value):
    result = parse_season_pass_validity(value)
    assert isinstance(result, str)


@given(st.one_of(st.text(), st.none()))
def test_compute_trail_gradient_safe(value):
    result = compute_trail_gradient(value)
    assert result is None or isinstance(result, float)


@given(st.one_of(st.text(), st.none()))
def test_calculate_lift_access_tier_safe(value):
    result = calculate_lift_access_tier(value)
    assert result is None or isinstance(result, float)


def test_valid_inputs_keep_expected_behavior():
    assert parse_season_pass_validity("2027/01/09") == (
        "Pass Expiry: 2027-01-09 (VALID)"
    )
    assert compute_trail_gradient("250:1000") == 25.0
    assert calculate_lift_access_tier(" int ") == 60.0


def test_invalid_inputs_are_rejected():
    assert parse_season_pass_validity("2026/02/31").startswith("Invalid pass expiry")
    assert compute_trail_gradient("10:0") is None
    assert calculate_lift_access_tier("unknown") is None
