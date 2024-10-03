"""Athan Library."""

import argparse
import calendar
import csv
import math
import tempfile
from datetime import date, datetime, timedelta
from typing import Dict, Optional


class Athan:
    """Calculate Basic Functions."""

    def __init__(
        self,
        elev: float = 96.3168,
        lat: float = 30,
        lon: float = -100,
        asr_method: int = 1,  # jumhoor. = 2 for hanafi
        fajr_angle: float = 15,
        isha_angle: float = 15,
    ) -> None:
        """Init Class.

        Args:
            elev (float, optional): Elevation or Altitude. Defaults to 96.3168.
            lat (float, optional): Latitude. Defaults to 30.
            lon (float, optional): Longitude. Defaults to -100.
            asr_method (int, optional): Asr Method. Defaults to 1 Jumhoor. Use 2 for Hanafi.
            fajr_angle (float, optional): Angle for Fajr rise Defaults to 15.
            isha_angle (float, optional): Angel for Isha. Defaults to 15.
        """
        self.elev = elev
        self.lat = lat
        self.lon = lon
        self.asr_method = asr_method
        self.fajr_angle = fajr_angle
        self.isha_angle = isha_angle

        self.today = date.today()
        self.year = self.today.year
        self.tz = datetime.now().astimezone().utcoffset() / timedelta(hours=1)  # type: ignore
        self.daysinyear = self.days_in_year(self.today.year)
        self.daynum = datetime.now().timetuple().tm_yday

    def days_in_year(self, year: int) -> int:
        """Number of days in a specific year.

        Args:
            year (int): Gregorian Year

        Returns:
            int: number of days in year
        """
        return 365 + calendar.isleap(year)

    def rad2deg(self, n: float) -> float:
        """Rad to degrees.

        Args:
            n (float): rad angle

        Returns:
            float: deg angle
        """
        return n * (180.0 / math.pi)

    def deg2rad(self, n: float) -> float:
        """Degrees to rad.

        Args:
            n (float): deg angle

        Returns:
            float: rad angle
        """
        return n * (math.pi / 180.0)

    def acot(self, n: float) -> float:
        """Trig Acot function.

        Args:
            n (float): angle

        Returns:
            float: acot of angle
        """
        return math.atan(1.0 / n)

    def sign(self, n: float) -> int:
        """Sign of a number.

        Args:
            n (float): a number

        Returns:
            int: positive or negative sign
        """
        if n >= 0:
            return 1
        else:
            return -1

    def date_from_day(self, year: int, day: int):
        """Get date from day number.

        Args:
            year (int): Gregorian Year
            day (int): Day Number in that year

        Returns:
            _type_: full date
        """
        return datetime(year, 1, 1) + timedelta(days=day - 1)

    def day_from_date(self, given_date):
        """Get the day number from a date.

        Args:
            given_date (_type_): full date

        Returns:
            int: day number
        """
        onejan = datetime(given_date.year, 1, 1)
        return (given_date - onejan).days + 1

    def hours_to_time(self, n: float) -> str:
        """Convert fractions of minutes or human readable minutes.

        Args:
            n (float): hour.minute_fraction

        Returns:
            str: HH:MM
        """
        hours = math.floor(n)
        mins = math.floor((n - hours) * 60)
        if hours > 12:
            hours -= 12
        if mins < 10:
            mins = "0" + str(mins)
        return f"{hours}:{mins}"

    def calc_times(
        self,
        day: int | None = None,
        alt: float | None = None,
        lat: float | None = None,
        lon: float | None = None,
        tz: float | None = None,
        asrmthd: int | None = None,
        gd: float | None = None,
        gn: float | None = None,
        days_in_year: int | None = None,
    ) -> Dict[str, float]:
        """Calculate Prayer Times.

        Args:
            day (int, optional): Day Number
            alt (float, optional): Elevation.
            lat (float, optional): Latitude.
            lon (float, optional): Longitude.
            tz (float, optional): timezone.
            asrmthd (int, optional): Asr Method. 1=Jumhoor, 2=Hanafi.
            gd (float, optional): Fajr Angle.
            gn (float, optional): Isha Angle.
            days_in_year (int, optional): Number of days in year.

        Returns:
             -> Dict[str, float]: Athan Times
        """
        day = self.daynum if day is None else day
        alt = self.elev if alt is None else alt
        lat = self.lat if lat is None else lat
        lon = self.lon if lon is None else lon
        tz = self.tz if tz is None else tz
        asrmthd = self.asr_method if asrmthd is None else asrmthd
        gd = self.fajr_angle if gd is None else gd
        gn = self.isha_angle if gn is None else gn
        days_in_year = self.daysinyear if days_in_year is None else days_in_year

        # see https://patents.google.com/patent/US20050237859A1/en
        # document above explains all equations in details
        beta = (2 * math.pi * day) / days_in_year
        d = (180.0 / math.pi) * (
            0.006918
            - (0.399912 * math.cos(beta))
            + (0.070257 * math.sin(beta))
            - (0.006758 * math.cos(2 * beta))
            + (0.000907 * math.sin(2 * beta))
            - (0.002697 * math.cos(3 * beta))
            + (0.001480 * math.sin(3 * beta))
        )
        t = 229.18 * (
            0.000075
            + (0.001868 * math.cos(beta))
            - (0.032077 * math.sin(beta))
            - (0.014615 * math.cos(2 * beta))
            - (0.040849 * math.sin(2 * beta))
        )
        r = 15.0 * tz
        z = 12.0 + ((r - lon) / 15.0) - (t / 60.0)

        xu = (
            math.sin(self.deg2rad(-0.8333 - 0.0347 * self.sign(alt) * math.sqrt(abs(alt))))
            - math.sin(self.deg2rad(d)) * math.sin(self.deg2rad(lat))
        ) / (math.cos(self.deg2rad(d)) * math.cos(self.deg2rad(lat)))

        u = None
        if -1 <= xu <= 1:
            u = self.rad2deg(1 / 15.0 * math.acos(xu))

        xvd = (
            -math.sin(self.deg2rad(gd)) - math.sin(self.deg2rad(d)) * math.sin(self.deg2rad(lat))
        ) / (math.cos(self.deg2rad(d)) * math.cos(self.deg2rad(lat)))
        vd = self.rad2deg(1 / 15.0 * math.acos(xvd))

        xvn = (
            -math.sin(self.deg2rad(gn)) - math.sin(self.deg2rad(d)) * math.sin(self.deg2rad(lat))
        ) / (math.cos(self.deg2rad(d)) * math.cos(self.deg2rad(lat)))
        vn = self.rad2deg(1 / 15.0 * math.acos(xvn))

        w = self.rad2deg(
            1
            / 15.0
            * math.acos(
                (
                    math.sin(
                        self.acot(asrmthd + math.tan(abs(self.deg2rad(lat) - self.deg2rad(d))))
                    )
                    - math.sin(self.deg2rad(d)) * math.sin(self.deg2rad(lat))
                )
                / (math.cos(self.deg2rad(d)) * math.cos(self.deg2rad(lat)))
            )
        )

        prayertimes = {}

        prayertimes["fajr"] = z - vd
        prayertimes["shuruq"] = z - u if u is not None else None
        prayertimes["dhur"] = z
        prayertimes["asr"] = z + w
        prayertimes["maghrib"] = z + u if u is not None else None
        prayertimes["isha"] = z + vn

        return prayertimes

    def year_athan_times(self, year: Optional[int] = None) -> list[list[str]]:
        """Generate Athan times for entire year.

        Args:
            year (int, optional): Gregorian year.

        Returns:
            list[list[str]]: prayer table for a specific Gregorian year.
        """
        thisyear = self.year if year is None else year
        daysinyear = self.days_in_year(thisyear)

        ptable = [["fajr", "shuruq", "thuhr", "asr", "maghrib", "isha", "tz"]]

        for daynum in range(1, daysinyear + 1):
            aday = self.date_from_day(thisyear, daynum)
            # set hours to 3:10AM to land on the correct timezone
            aday = aday.replace(hour=3, minute=10)
            tz = aday.astimezone().utcoffset() / timedelta(hours=1)  # type: ignore

            m_times = self.calc_times(day=daynum, tz=tz, days_in_year=daysinyear)
            ptable.append(
                [
                    self.hours_to_time(m_times["fajr"]),
                    self.hours_to_time(m_times["shuruq"]),
                    self.hours_to_time(m_times["dhur"]),
                    self.hours_to_time(m_times["asr"]),
                    self.hours_to_time(m_times["maghrib"]),
                    self.hours_to_time(m_times["isha"]),
                    str(tz),
                ]
            )

        return ptable

    def get_next_athan_time(self, salah: str, day: int | None = None) -> float:
        """Get next athan time given a prayer name.

        Args:
            salah (str): prayer name e.g. fajr, dhur, asr, maghrib, isha
            day (int | None, optional): Day Number. default to current day number when Athan() was
            constructed.

        Returns:
            float: athan time in hh.franction format.
        """
        day = self.daynum if day is None else day

        # get prayer times
        m_times = self.calc_times(day=day)
        return m_times[salah]

    def get_next_salah(self, m_times: Dict[str, float]):
        """Determine the next salah.

        Args:
            m_times (Dict[str, float]): prayer table

        Returns:
            str: fajr, dhur, asr, maghrib, isha
        """
        # get today's date/time
        today = datetime.now()
        tommr = today + timedelta(days=1)
        nextday = tommr.timetuple().tm_yday

        # remove shuruq calculation. it is not needed for athan calls
        m_times.pop("shuruq", None)

        # get time in float hours for easier comparison with calc_times() returns
        float_hours = today.hour + today.minute / 60 + today.second / 3600

        next_salah = None
        # loop over all prayers to find next call. if not found, we will calculate tomorrow's table
        for salah, athan_time in m_times.items():
            if float_hours < athan_time:
                next_salah = salah
                next_call_time = m_times[next_salah]
                # get athan hour, minute, second
                a_hour = int(next_call_time)
                a_fraction = next_call_time - a_hour
                a_mins = int(a_fraction * 60)
                a_secs = int((a_fraction * 60 - a_mins) * 60)

                athan_time = datetime(today.year, today.month, today.day, a_hour, a_mins, a_secs)
                break

        # past isha time, get fajr time.
        if not next_salah:
            next_salah = "fajr"
            next_call_time = self.get_next_athan_time(next_salah, nextday)
            # get athan hour, minute, second
            a_hour = int(next_call_time)
            a_fraction = next_call_time - a_hour
            a_mins = int(a_fraction * 60)
            a_secs = int((a_fraction * 60 - a_mins) * 60)

            athan_time = datetime(tommr.year, tommr.month, tommr.day, a_hour, a_mins, a_secs)

        return athan_time, next_salah  # type: ignore


def get_prayer_times(prayer: Athan) -> Dict[str, float]:
    """Calculate and print prayer times.

    Args:
        prayer (Athan): _description_

    Returns:
        Dict[str, float]: prayer times Dict
    """
    # get prayer times for today
    m_times = prayer.calc_times()

    print("Fajr: " + str(timedelta(hours=m_times["fajr"])))
    print("Shuruq: " + str(timedelta(hours=m_times["shuruq"])))
    print("Dhur: " + str(timedelta(hours=m_times["dhur"])))
    print("Asr: " + str(timedelta(hours=m_times["asr"])))
    print("Maghrib: " + str(timedelta(hours=m_times["maghrib"])))
    print("Isha: " + str(timedelta(hours=m_times["isha"])))

    athan_time, next_salah = prayer.get_next_salah(m_times)
    print(f"Next {next_salah} Athan will be called @ {athan_time}")

    return m_times


def print_prayer_times(m_times: Dict[str, float]):
    """Determine the next salah.

    Args:
        m_times (Dict[str, float]): prayer table
    """
    print("Fajr: " + str(timedelta(hours=m_times["fajr"])))
    print("Shuruq: " + str(timedelta(hours=m_times["shuruq"])))
    print("Dhur: " + str(timedelta(hours=m_times["dhur"])))
    print("Asr: " + str(timedelta(hours=m_times["asr"])))
    print("Maghrib: " + str(timedelta(hours=m_times["maghrib"])))
    print("Isha: " + str(timedelta(hours=m_times["isha"])))


def generate_year_prayer_times(prayer: Athan, year: int) -> str:
    """Generate a csv prayer table for entire gregorian year.

    Args:
        prayer (Athan): Object contain Athan()
        year (int): year as in YYYY

    Returns:
        str: csv file path
    """
    year_athans = prayer.year_athan_times(year)

    with tempfile.NamedTemporaryFile(
        mode="w", prefix=f"Athan_{year}", suffix=".csv", delete=False
    ) as tf:
        csv_writer = csv.writer(tf)
        csv_writer.writerows(year_athans)
        print("Athan times written to " + tf.name)

    return tf.name


def start():
    """Entry Point for CLI."""
    parser = argparse.ArgumentParser(description="Schedule Athan Times.")
    parser.add_argument("-e", "--elev", type=float, default=100, help="Elevation in meters")
    parser.add_argument("-l", "--lat", type=float, default=30, help="Latitude in degrees")
    parser.add_argument("-L", "--lon", type=float, default=-120, help="Longitude in degrees")
    parser.add_argument("-a", "--asr", type=int, default=1, help="Asr (1: Jumhoor, 2: Hanafi)")
    parser.add_argument("-f", "--fajr_angle", type=float, default=15, help="Fajr angle in degrees")
    parser.add_argument("-i", "--isha_angle", type=float, default=15, help="Isha angle in degrees")

    args = parser.parse_args()

    # init Athan() class
    prayer = Athan(
        elev=args.elev,
        lat=args.lat,
        lon=args.lon,
        asr_method=args.asr,  # jumhoor = 1. hanafi = 2
        fajr_angle=args.fajr_angle,
        isha_angle=args.isha_angle,
    )

    # example prayer calculation
    get_prayer_times(prayer)


if __name__ == "__main__":
    # init Athan() class
    prayer = Athan(
        elev=100,
        lat=30,
        lon=-120,
        asr_method=1,  # jumhoor = 1. hanafi = 2
        fajr_angle=15,
        isha_angle=15,
    )

    # example prayer calculation
    get_prayer_times(prayer)
    # generate a csv file for entire gregorian year
    generate_year_prayer_times(prayer, 2025)
