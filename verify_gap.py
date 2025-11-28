import json
from datetime import datetime, timedelta


def verify_gaps():
    with open("data.json", "r") as f:
        data = json.load(f)

    dates = [datetime.strptime(d["date"], "%Y-%m-%d") for d in data]
    dates.sort()

    max_gap = timedelta(days=0)
    gap_threshold = timedelta(days=5)  # Allow for weekends and long weekends
    gaps_found = []

    for i in range(1, len(dates)):
        diff = dates[i] - dates[i - 1]
        if diff > max_gap:
            max_gap = diff

        if diff > gap_threshold:
            gaps_found.append(
                (
                    dates[i - 1].strftime("%Y-%m-%d"),
                    dates[i].strftime("%Y-%m-%d"),
                    diff.days,
                )
            )

    print(f"Total data points: {len(dates)}")
    print(f"Start Date: {dates[0].strftime('%Y-%m-%d')}")
    print(f"End Date: {dates[-1].strftime('%Y-%m-%d')}")
    print(f"Max gap observed: {max_gap.days} days")

    if gaps_found:
        print("Gaps found (> 5 days):")
        for start, end, days in gaps_found:
            print(f"  Gap between {start} and {end}: {days} days")
    else:
        print("No significant gaps found.")

    # Specific check for the user-reported gap period
    check_start = datetime(1999, 12, 1)
    check_end = datetime(2000, 8, 30)

    points_in_period = [d for d in dates if check_start <= d <= check_end]
    print(
        f"Data points between {check_start.strftime('%Y-%m-%d')} and {check_end.strftime('%Y-%m-%d')}: {len(points_in_period)}"
    )


if __name__ == "__main__":
    verify_gaps()
