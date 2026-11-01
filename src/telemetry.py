import pandas as pd


def compare_drivers(laps):
    if laps.empty:
        return pd.DataFrame()

    data = laps.copy()

    data["driver_number"] = (
        data["driver_number"].astype(str)
    )

    data["lap_duration"] = pd.to_numeric(
        data["lap_duration"],
        errors="coerce"
    )

    data = data.dropna(
        subset=["driver_number", "lap_duration"]
    )

    result = (
        data.groupby("driver_number")["lap_duration"]
        .agg(["mean", "min", "count"])
        .reset_index()
    )

    result = result.rename(
        columns={
            "driver_number": "Driver",
            "mean": "Average Lap (s)",
            "min": "Best Lap (s)",
            "count": "Valid Laps"
        }
    )

    return result.sort_values(
        "Average Lap (s)",
        ascending=True
    )


def compare_two_drivers(laps, driver_1, driver_2):
    if laps.empty:
        return pd.DataFrame()

    data = laps.copy()

    data["driver_number"] = (
        data["driver_number"].astype(str)
    )

    data["lap_duration"] = pd.to_numeric(
        data["lap_duration"],
        errors="coerce"
    )

    first = data[
        data["driver_number"] == str(driver_1)
    ][["lap_number", "lap_duration"]].rename(
        columns={"lap_duration": "Driver 1"}
    )

    second = data[
        data["driver_number"] == str(driver_2)
    ][["lap_number", "lap_duration"]].rename(
        columns={"lap_duration": "Driver 2"}
    )

    comparison = pd.merge(
        first,
        second,
        on="lap_number",
        how="inner"
    )

    comparison = comparison.dropna()

    comparison["Time Difference (s)"] = (
        comparison["Driver 1"] - comparison["Driver 2"]
    )

    return comparison.sort_values("lap_number")