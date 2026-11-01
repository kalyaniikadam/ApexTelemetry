import pandas as pd
import matplotlib.pyplot as plt


def prepare_speed_data(telemetry):
    if telemetry.empty:
        raise ValueError(
            "No telemetry data available for this driver."
        )

    data = telemetry.copy()

    data["speed"] = pd.to_numeric(
        data["speed"],
        errors="coerce"
    )

    data["date"] = pd.to_datetime(
        data["date"],
        errors="coerce"
    )

    data = data.dropna(
        subset=["date", "speed"]
    )

    data = data.sort_values("date")

    if data.empty:
        raise ValueError(
            "No valid speed measurements found."
        )

    return data


def plot_speed_telemetry(speed_data, driver_name):

    fig, ax = plt.subplots(figsize=(13, 5))

    fig.patch.set_facecolor("#0B1115")
    ax.set_facecolor("#121D23")

    ax.plot(
        speed_data["date"],
        speed_data["speed"],
        color="#00D2BE",
        linewidth=2
    )

    ax.fill_between(
        speed_data["date"],
        speed_data["speed"],
        color="#00D2BE",
        alpha=0.14
    )

    ax.set_title(
        f"SPEED TELEMETRY | {driver_name}",
        color="white",
        fontsize=17,
        fontweight="bold",
        pad=20
    )

    ax.set_xlabel(
        "TIME",
        color="#B8C9CC",
        fontsize=10
    )

    ax.set_ylabel(
        "SPEED (KM/H)",
        color="#B8C9CC",
        fontsize=10
    )

    ax.tick_params(colors="white")

    ax.grid(
        color="#789096",
        alpha=0.18,
        linestyle="--"
    )

    for spine in ax.spines.values():
        spine.set_color("#30454B")

    fig.autofmt_xdate()
    plt.tight_layout()

    return fig