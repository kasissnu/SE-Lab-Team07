"""Input-safe ski resort pass processing helpers."""

from datetime import date
import math


def parse_season_pass_validity(date_str):
    """Format a YYYY/MM/DD expiry date, or describe invalid input."""
    if not isinstance(date_str, str):
        return "Invalid pass expiry: expected YYYY/MM/DD"

    parts = date_str.strip().split("/")
    if len(parts) != 3:
        return "Invalid pass expiry: expected YYYY/MM/DD"

    try:
        year, month, day = (int(part.strip()) for part in parts)
        date(year, month, day)
    except (TypeError, ValueError, OverflowError):
        return "Invalid pass expiry: expected a real YYYY/MM/DD date"

    valid = year >= 2026
    return f"Pass Expiry: {year:04d}-{month:02d}-{day:02d} ({'VALID' if valid else 'EXPIRED'})"


def compute_trail_gradient(elevation_str):
    """Return trail gradient percentage, or None for invalid measurements."""
    if not isinstance(elevation_str, str):
        return None

    parts = elevation_str.strip().split(":")
    if len(parts) != 2:
        return None

    try:
        drop, distance = (float(part.strip()) for part in parts)
    except (TypeError, ValueError, OverflowError):
        return None

    if not math.isfinite(drop) or not math.isfinite(distance):
        return None
    if drop < 0 or distance <= 0:
        return None

    return round((drop / distance) * 100.0, 2)


def calculate_lift_access_tier(zone_code):
    """Return a lift pass price, or None for an unknown zone code."""
    if not isinstance(zone_code, str):
        return None

    prefix = zone_code.strip().upper()[:3]
    zone_rates = {
        "BEG": 35.0,
        "INT": 60.0,
        "ADV": 85.0,
        "ALL": 110.0,
    }
    return zone_rates.get(prefix)


def main():
    print("==== Running parse_season_pass_validity ====")
    d_input = input("Enter pass expiry (YYYY/MM/DD): ")
    print(parse_season_pass_validity(d_input))

    print("\n==== Running compute_trail_gradient ====")
    e_input = input("Enter drop:distance (e.g. 250:1000): ")
    print("Gradient %:", compute_trail_gradient(e_input))

    print("\n==== Running calculate_lift_access_tier ====")
    z_input = input("Enter zone code (e.g. BEG, INT, ALL): ")
    print("Lift Pass Price: $", calculate_lift_access_tier(z_input))


if __name__ == "__main__":
    main()
