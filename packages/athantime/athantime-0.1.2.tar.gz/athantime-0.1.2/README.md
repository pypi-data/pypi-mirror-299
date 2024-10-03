# Zero external dependency Athan calculator
A simple Athan calculator with no external dependencies. Calculates prayer times using latitude, longitude, and elevation.

### Usage
```python
from athantimes import Athan, print_prayer_times

# create Athan object based on user params
prayer = Athan(
    elev=100,  # Elevation
    lat=30,  # Latitude
    lon=-100  # Longitude
    # asr_method=1,  # jumhoor = 1. hanafi = 2
    # fajr_angle=15,
    # isha_angle=15,
)

# calculate athan times
m_times = prayer.calc_times()

# print prayer table
print_prayer_times(m_times)

# figure out next salah time
athan_time, next_salah = prayer.get_next_salah(m_times)
print(f"Next Athan ({next_salah}) will be called @ {athan_time}")
```

Output:
```
Fajr: 4:22:55.791533
Shuruq: 5:27:00.491693
Dhur: 11:31:53.542215
Asr: 14:58:52.500350
Maghrib: 17:36:46.592737
Isha: 18:40:51.292898

Next Athan (fajr) will be called @ 2024-09-24 04:23:30
```

- See `examples` directory for additional usage. 
- `sched_athan.py` is an example running the library as a background process which execute a command 
every time an Athan is called. This is useful if you want to play an audio file.

#### Example Athan Schedule
Assuming there is a shell script which plays audios, a user can play all 5 Athans using this command
```
python3 examples/sched_athan.py -e 100 -l 30 -L -100

where -e is elevation, -l is longitude, and -L is longitude
```
