from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import pandas as pd

from .db import ROOT, run_query

FIGURES_DIR = ROOT / "figures"

BLUE = "#2b6cb0"
LIGHT_BLUE = "#a9c6e8"
ORANGE = "#d9822b"
GREY = "#8a8f98"
MONTHS = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]


def _style(ax, title, xlabel, ylabel):
    ax.set_title(title, loc="left", fontsize=12, fontweight="bold")
    ax.set_xlabel(xlabel)
    ax.set_ylabel(ylabel)
    ax.spines[["top", "right"]].set_visible(False)
    ax.grid(axis="y", alpha=0.25)


def _save(fig, name, out_dir):
    out_dir.mkdir(exist_ok=True)
    path = out_dir / name
    fig.tight_layout()
    fig.savefig(path, dpi=150)
    plt.close(fig)
    return path


def daily_energy(db_path, out_dir):
    df = run_query("05_rolling_7day", db_path)
    df["day"] = pd.to_datetime(df["day"])
    # reindex so days dropped for missing data show as breaks
    df = df.set_index("day").reindex(pd.date_range(df["day"].min(), df["day"].max()))

    fig, ax = plt.subplots(figsize=(10, 4))
    ax.plot(df.index, df["kwh"], color=LIGHT_BLUE, linewidth=0.8, label="Daily total")
    ax.plot(df.index, df["kwh_7d_avg"], color=BLUE, linewidth=1.5, label="7-day average")
    _style(ax, "Daily energy use", "", "kWh per day")
    ax.legend(frameon=False)
    return _save(fig, "daily_energy.png", out_dir)


def hourly_profile(db_path, out_dir):
    df = run_query("02_hourly_profile", db_path)
    fig, ax = plt.subplots(figsize=(8, 4))
    for day_type, colour in (("weekday", BLUE), ("weekend", ORANGE)):
        part = df[df["day_type"] == day_type]
        ax.plot(part["hour"], part["avg_kw"], color=colour, linewidth=2, label=day_type.capitalize())
    ax.set_xticks(range(0, 24, 3))
    _style(ax, "Average power by hour of day", "Hour", "kW")
    ax.legend(frameon=False)
    return _save(fig, "hourly_profile.png", out_dir)


def seasonality(db_path, out_dir):
    df = run_query("03_monthly_seasonality", db_path)
    fig, ax = plt.subplots(figsize=(8, 4))
    ax.bar([MONTHS[m - 1] for m in df["month"]], df["avg_daily_kwh"], color=BLUE)
    _style(ax, "Average daily energy by month", "", "kWh per day")
    return _save(fig, "seasonality.png", out_dir)


def submetering(db_path, out_dir):
    df = run_query("07_submetering_share", db_path)
    parts = [("kitchen_pct", "Kitchen", BLUE), ("laundry_pct", "Laundry room", ORANGE),
             ("heating_pct", "Water heater and AC", "#4a9d8f"), ("other_pct", "Not sub-metered", GREY)]
    fig, ax = plt.subplots(figsize=(8, 4))
    bottom = pd.Series(0.0, index=df.index)
    for column, label, colour in parts:
        ax.bar(df["year"], df[column], bottom=bottom, color=colour, label=label)
        bottom += df[column]
    _style(ax, "Share of energy by sub-meter", "", "% of total")
    ax.legend(frameon=False, loc="center left", bbox_to_anchor=(1, 0.5))
    return _save(fig, "submetering.png", out_dir)


def make_all(db_path, out_dir=FIGURES_DIR):
    out_dir = Path(out_dir)
    return [daily_energy(db_path, out_dir), hourly_profile(db_path, out_dir),
            seasonality(db_path, out_dir), submetering(db_path, out_dir)]
