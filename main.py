'''
Purpose: find date when Jupiter and Saturn are both in the sky
         during the afternoon (15:30 local time)

Requirements:
- Accurate rise/set visibility windows
- DST-aware timezone handling
- Ensure rise/set belong to the same cycle

Returns:
- Dates when Jupiter and Saturn are visible at 15:30
- Individual visibility sets
- Their intersection
'''

from astronomy import *
from datetime import datetime, timedelta, timezone
from zoneinfo import ZoneInfo

def isBetween(cur, start, end):
    """Check if `cur` is between `start` and `end`, accounting for overnight spans."""
    if start <= end:
        return start <= cur <= end
    else:
        return cur >= start or cur <= end

def planetDays(iBody: Body, location: dict, wedding: dict) -> set:
    planet_set = set()

    observer = Observer(location["lat"], location["long"], location["height"])
    tz = location["tz"]

    for day in search_days:
        # Build target wedding time (local and UTC)
        iDate = Time.Utc(day)
        wedding_local = datetime(iDate.year, iDate.month, iDate.day, 
                                  wedding["hour"], wedding["min"], tzinfo=tz)
        wedding_utc = wedding_local.astimezone(timezone.utc)

        # Step 1: find most recent rise before wedding time
        rise_time = SearchRiseSet(
            body=iBody,
            observer=observer,
            direction=Direction.Rise,
            startTime=day.AddDays(-1),
            limitDays=3
        )
        rise_utc = Time.Utc(rise_time).astimezone(timezone.utc)

        # Step 2: find set after that rise
        set_time = SearchRiseSet(
            body=iBody,
            observer=observer,
            direction=Direction.Set,
            startTime=rise_time,
            limitDays=2
        )
        set_utc = Time.Utc(set_time).astimezone(timezone.utc)

        #print(wedding_utc, rise_utc, set_utc)

        # Step 3: is the planet up at wedding time?
        if isBetween(wedding_utc, rise_utc, set_utc):
            confirm_date = wedding_local.date().isoformat()
            planet_set.add(confirm_date)
            print(day, wedding_utc, rise_utc, set_utc)

    return planet_set

# ---------------------------
# CONFIGURATION
# ---------------------------

# Date range: Jan 1, 2026 → Jan 1, 2028
YEAR = 365
NEED_DAY = 9497  # corresponds to 2000-01-01 + 9497 = 2026-01-01
END_DAY = NEED_DAY + 2 * YEAR

search_days = [Time(x) for x in range(NEED_DAY, END_DAY)]

# Target time of day (local)
wedding = {"hour": 15, "min": 30}

# Location: Los Angeles
tz_la = ZoneInfo("America/Los_Angeles")
LA = {
    "lat": 34.0522,
    "long": -118.2426,
    "height": 0,
    "tz": tz_la
}

# ---------------------------
# COMPUTATION
# ---------------------------

jupiter_set = planetDays(Body.Jupiter, location=LA, wedding=wedding)
saturn_set = planetDays(Body.Saturn, location=LA, wedding=wedding)
both_visible = jupiter_set & saturn_set

# ---------------------------
# OUTPUT
# ---------------------------

print("Dates Jupiter is visible at 15:30:")
for date in sorted(jupiter_set):
    print(date)

print("\nDates Saturn is visible at 15:30:")
for date in sorted(saturn_set):
    print(date)

print("\nDates BOTH are visible at 15:30:")
for date in sorted(both_visible):
    print(date)

