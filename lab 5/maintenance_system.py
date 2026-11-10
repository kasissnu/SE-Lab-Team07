"""Track warehouse assets and identify equipment due for inspection."""

import json
import tempfile
from datetime import datetime, timedelta

# Global state
assets = {}
settings = {"service_interval_days": 90}


def register_asset(asset_id, machine_type, logs=None):
    """Register an asset and record the registration for this run."""
    if logs is None:
        logs = []
    assets[asset_id] = {
        "type": machine_type,
        "last_service": datetime.now().strftime("%Y-%m-%d"),
    }
    logs.append(asset_id)
    print("Registered", asset_id, "- total registrations this run:", len(logs))


def update_service_date(asset_id, date):
    """Update an existing asset's service date after validating its format."""
    try:
        datetime.strptime(date, "%Y-%m-%d")
        assets[asset_id]["last_service"] = date
    except (KeyError, ValueError):
        print("Could not update", asset_id, "with date", date)


def due_for_inspection():
    """Return asset IDs whose last service is outside the service interval."""
    due = []
    now = datetime.now()
    for asset_id, asset in assets.items():
        last = datetime.strptime(asset["last_service"], "%Y-%m-%d")
        if now - last > timedelta(days=settings["service_interval_days"]):
            due.append(asset_id)
    return due


def change_interval(days):
    """Set the number of days between required inspections."""
    if days <= 0:
        raise ValueError("Inspection interval must be positive")
    settings["service_interval_days"] = days


def export_service_report(file_name="maintenance.json"):
    """Write the current registry to a UTF-8 JSON report."""
    with open(file_name, "w", encoding="utf-8") as report_file:
        json.dump(assets, report_file, indent=2)
    print("Report written to " + file_name)


def write_scratch_copy():
    """Write a safe, uniquely named temporary copy of the registry."""
    with tempfile.NamedTemporaryFile(
        mode="w", suffix=".json", encoding="utf-8", delete=False
    ) as scratch_file:
        json.dump(assets, scratch_file)
        path = scratch_file.name
    print("Scratch copy at", path)


def print_alerts():
    """Print an alert for each asset overdue for inspection."""
    for asset_id in due_for_inspection():
        print(
            "ALERT: inspection overdue for", asset_id, assets[asset_id]["type"]
        )


def main():
    """Run the sample maintenance registry workflow."""
    registration_log = []
    register_asset("FL-01", "Forklift", registration_log)
    register_asset("CV-07", "Conveyor", registration_log)
    register_asset("", "Pallet Jack", registration_log)
    register_asset("FL-01", "Crane", registration_log)
    update_service_date("FL-01", "2025-01-15")
    update_service_date("XX-99", "2025-02-01")
    change_interval(30)
    d = input("Last service date for CV-07 (YYYY-MM-DD, Enter to skip): ")
    if d:
        update_service_date("CV-07", d)
    if not assets:
        raise RuntimeError("No assets registered")
    print_alerts()
    export_service_report()
    write_scratch_copy()


if __name__ == "__main__":
    main()
