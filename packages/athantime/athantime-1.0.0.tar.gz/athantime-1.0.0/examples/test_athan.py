"""Simple example using elevation, latitude, longitude."""

from athantime import Athan, print_prayer_times

# create Athan object based on user params
prayer = Athan(
    elev=100,  # Elevation
    lat=30,  # Latitude
    lon=-100,  # Longitude
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
