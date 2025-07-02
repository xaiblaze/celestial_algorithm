from skyfield.api import load, Topos
from datetime import datetime
from pytz import timezone

eph = load('de421.bsp')
planets = [eph['JUPITER BARYCENTER'], eph['SATURN BARYCENTER']]
ts = load.timescale()

observer = Topos(
    latitude_degrees=34.05,
    longitude_degrees=-118.25
)

pacific = timezone('US/Pacific')

t0 = ts.utc(2026, 1, 1)
t1 = ts.utc(2028, 1, 1)


# find rise/set for all planets
from skyfield.almanac import find_discrete, risings_and_settings
for p in planets:
    interval = []
    f = risings_and_settings(eph, p, observer)

    #https://in-the-sky.org/whatsup_times.php


    times, events = find_discrete(t0, t1, f)
    for t, e in zip(times, events):
        print(t.astimezone(pacific), "Rise" if e else "Set")

    print()


