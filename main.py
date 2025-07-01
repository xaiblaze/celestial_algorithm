'''
Purpose: find date when Jupiter and Saturn are both in the sky
         during the morning

need: precise location

given a rise and set time, is the need time inside?


return all dates where both J and S are in the sky at 15:30
 -  return dates with J and S separately
 -  return union


 alternate: return dates of Jupiter and Saturn aphelion? Unlikely they'll coincide

'''


from astronomy import *
from datetime import datetime, timezone, timedelta

def isBetween(cur, start, end):
    return cur >= start and cur <= end

def planetDays(iBody: Body) -> set:

    planet_set = set()

    for day in search_days:
        # create target time for iDay
        # check if between rise and set time
        interval = {}
        for elem in iDirections:
            result = SearchRiseSet(body=iBody, observer=iObserver, 
                        direction=elem, startTime=day, limitDays=iLimitDays)
            result_utc = Time.Utc(result)
            #print(elem, result_utc.astimezone(tz_pdt))
            interval[elem] = result_utc

        #print(interval)
        iDate = Time.Utc(day)
        iYear = iDate.year
        iDay = iDate.day
        iMonth = iDate.month 
        iSecond = 0 # dont care about sec

        wedding_time = datetime(iYear, iMonth, iDay, WEDDING_HOUR,
                                WEDDING_MIN, iSecond)
        
        confirm_day = interval[Direction.Rise]
        confirm_date = f"{confirm_day.year}/{confirm_day.month}/{confirm_day.day}"

        planet_set.add(confirm_date) if isBetween(wedding_time, interval[Direction.Rise], interval[Direction.Set]) else None

    return planet_set

# 9497: 1 Jan 2000 to 1 Jan 2026 
YEAR = 365
NEED_DAY = 9497
END_DAY = NEED_DAY + 2*YEAR

search_days = [Time(x) for x in range(NEED_DAY, END_DAY)]

tz_utc = timezone.utc
tz_pdt = timezone(timedelta(hours=-7))
WEDDING_HOUR = 15
WEDDING_MIN = 30


# LOS ANGELES (PDT offset UTC-7)
lat = 34.0522
long = 118.2426
height = 0


iBody = Body.Jupiter
iObserver = Observer(lat, long, height)
iDirections = [Direction.Rise, Direction.Set]
iLimitDays = 1


jupiter_set = planetDays(Body.Jupiter)
#print(sorted(jupiter_set))
print()
saturn_set = planetDays(Body.Saturn)
#print(sorted(saturn_set))
#print(saturn_set)

jupiter_saturn_set = jupiter_set.intersection(saturn_set)

[print(f"{elem}") for elem in sorted(jupiter_saturn_set)]
    