# ufostalker
Simple way to access ufostalker via python. Only dependency is `requests`.

A couple of examples:
```py
from ufostalker import UFOCase
some_case = UFOCase(94216)

print(some_case)
>>> Case #94216 in Fremont, Indiana

print(some_case.summary)
>>> Bright red circular objaect that just appeared and disappeared

print(some_case.url)
>>> http://www.ufostalker.com/sighting/94216

print(some_case.specifics.shape)
>>> Circle

print(some_case.location.coordinates)
>>> -84.96002532489504, 41.73339344126648

print(some_case.weather)
>>> Temperature: 22C; Visibility: 11km; Conditions: Rain

print(some_case.occurred)
>>> 2018-08-16 00:00:00



# You can also change the ID and all the case info updates:
some_case.id = 5002

print(some_case)
>>> Case #5002 in Oklahoma

print(some_case.submitted)
>>> 2006-06-27 22:15:00

# Note: The times provided with .occured and .submitted are in UTC, 
# this is just the timezone this sighting too place in.
print(or_some_other_case.timezone)
>>> America/North_Dakota/Center

# Weather can often be None, as UFOStalker isn't able to get the
# weather in for all cases. This is the daily average weather,
# and is not submitted by the submitter.
print(or_some_other_case.weather)
>>> None
```

There are a bunch more properties that I didn't show in the example, but I'm sure you can find that yourself.

You can also get a feed of all the UFO posts:
```py
from ufostalker import UFOFeed

# This is how you would print the next 10 UFO sighting that some up to console.
for case in UFOFeed(skip_existing=True, stop_after=10):
    print(case)

# This is how you would print the 5 latest cases and 5 to-be-submitted cases to console.
for case in UFOFeed(skip_existing=False, count=5, stop_after=10):
    print(case)

# This is how you would print the last page of cases and all the future cases that will ever be submitted in the future (provided the script keeps running).
for case in UFOFeed():
    print(case)
```