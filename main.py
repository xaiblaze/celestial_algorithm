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
from zoneinfo import ZoneInfo

def isBetween(cur, start, end):
    if start <= end:
        return start <= cur <= end
    else:
        # The object is up across midnight
        return cur >= start or cur <= end

def planetDays(iBody: Body, location: dict, wedding: dict) -> set:

    planet_set = set()

    iObserver = Observer(location["lat"], 
                         location["long"],
                         location["height"])
    iDirections = [Direction.Rise, Direction.Set]
    iLimitDays = 1      

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

        wedding_time_pdt = datetime(iYear, iMonth, iDay, wedding["hour"], 
                                    wedding["min"], tzinfo=location["tz"])

        local_day = wedding_time_pdt.date()
        confirm_date = f"{local_day.year}/{local_day.month}/{local_day.day}" 

        if isBetween(wedding_time_pdt, 
                     interval[Direction.Rise].astimezone(location["tz"]), 
                     interval[Direction.Set].astimezone(location["tz"])):
            
            planet_set.add(confirm_date) 

    return planet_set

# 9497: 1 Jan 2000 to 1 Jan 2026 
YEAR = 365
NEED_DAY = 9497
END_DAY = NEED_DAY + 2*YEAR

search_days = [Time(x) for x in range(NEED_DAY, END_DAY)]

tz_utc = timezone.utc


wedding = {"hour": 15, "min": 30}

# LA
tz_la = ZoneInfo('America/Los_Angeles')
LA = {"lat":34.0522, "long":-118.2426, "height": 0, "tz":tz_la}


jupiter_set = planetDays(Body.Jupiter,location=LA, wedding=wedding)
#print("jupiter ,", sorted(jupiter_set))
print()
saturn_set = planetDays(Body.Saturn, location=LA, wedding=wedding)
#print("saturn, ", sorted(saturn_set))
#print(saturn_set)

jupiter_saturn_set = jupiter_set.intersection(saturn_set)

[print(f"{elem}") for elem in sorted(jupiter_saturn_set)]
    