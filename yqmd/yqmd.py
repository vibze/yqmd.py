import calendar
from datetime import datetime, timedelta
import re
from dateutil.relativedelta import relativedelta


patterns = [

]


class Period(object):
    """
    # Create a sequence

    >>> Quarter.sequence('01.01.2014', '01.01.2015')
    [Quarter: Q1.2014, Quarter: Q2.2014, Quarter: Q2.2014, Quarter: Q3.2014, Quarter: Q1.2015]
    >>> Day.sequence(datetime(2015, 1, 29), datetime(2015, 2, 2))
    [Day: 29.01.2015, Day: 30.01.2015, Day: 31.01.2015, Day: 01.02.2015, Day: 02.02.2015]

    # Parse string
    >>> Month.parse('01 12 2014', '%d %m %Y')
    Month: 12.2014

    # Instantiate using datetime instance
    >>> Year(datetime(2015, 1, 15))
    Year: 2015

    # Instantiate with string
    # YYYY-MM-DD. Separator can be hyphen, dot or slash
    >>> Quarter('2013-05-06')
    Quarter: Q2.2013

    # DD-MM-YYYY. Separator can be hyphen dot or slash
    >>> Day('05-05-1985')
    Day: 05.05.1985

    # You can use 2 symbols for year, if the date is in 2000s
    >>> Day('05-05-85')
    Day: 05.05.2085

    # YYYY-MM-DD
    >>> Week('20130301')
    Week: W9.2013

    # DDMMYYYY
    >>> Month('05051985')
    Month: 05.1985

    # Numbers that fit in format are accepted too
    >>> Week(20130301)
    Week: W9.2013

    # You can get current period without passing any parameters
    >>> Month()
    Month: 05.2015

    # Shifting
    >>> day = Day('14.02.2014')
    >>> day
    Day: 14.02.2014
    >>> day.next()
    Day: 15.02.2014
    >>> day.next(5)
    Day: 20.02.2014
    >>> day.prev(2)
    Day: 18.02.2014
    >>> day.shift(4)
    Day: 22.02.2014
    >>> day.shift(-21)
    Day: 01.02.2014

    # Cloning
    >>> month = Month('05.05.1985')
    >>> month
    Month: 05.1985
    >>> month.next()
    Month: 06.1985
    >>> month.clone().next(5)
    Month: 11.1985
    >>> month
    Month: 06.1985

    # Formatting period representation
    >>> month = Month('05.05.1985')
    >>> month.format('%Y%m')
    '198505'

    # Gettings start/end of period
    >>> quarter = Quarter(20150606)
    >>> quarter
    Quarter: Q2.2015
    >>> quarter.start('%d.%m.%Y')
    '01.04.2015'
    >>> quarter.end()
    datetime.datetime(2015, 6, 30, 23, 59, 59, 999999)
    >>> quarter.range('%d-%m-%Y')
    ['01-04-2015', '30-06-2015']

    # Periods also have numeric attributes representing year/quarter/month/week/day if it's possible.
    # For example year only has `year` attribute and month has `year`, `quarter` and `month` attributes.
    """
    @classmethod
    def sequence(cls, start, end):
        start = cls(start)
        end = cls(end)

        seq = [start]
        while start != end:
            start = start.clone().next()
            seq.append(start)
        return seq

    @classmethod
    def parse(cls, text, format):
        return cls(datetime.strptime(str(text), format))

    def __init__(self, dt=None):
        if dt is None:
            self.datetime = datetime.now()

        if isinstance(dt, datetime):
            self.datetime = dt

        if isinstance(dt, int):
            dt = str(dt)

        if isinstance(dt, str):
            datere = re.compile(r"""
                (?:\s*)
                (?P<iso>
                  (?P<iso_yr>[12]\d{3})
                  (?P<sep>[-\./\s])
                  (?P<iso_mnth>0[1-9]|1[012]|[1-9])
                  (?P=sep)
                  (?P<iso_day>3[01]|[12]\d|0[1-9]|[1-9]))
                |(?P<dmy>
                  (?P<dmy_day>3[01]|[12]\d|0[1-9]|\d)
                  (?P<dmy_sep>[-\.\/\s])
                  (?P<dmy_mnth>0[1-9]|1[012]|\d)
                  (?P=dmy_sep)
                  (?P<dmy_yr>[12]\d{3}))
                |(?P<nsp>
                  (?P<nsp_day>3[01]|[12]\d|0[1-9])
                  (?P<nsp_mnth>0[1-9]|1[012])
                  (?P<nsp_yr>[12]\d{3}))
                |(?P<isonsp>
                  (?P<isonsp_yr>20[1-5]\d)
                  (?P<isonsp_mnth>0[1-9]|1[012])
                  (?P<isonsp_day>3[01]|[12]\d|0[1-9]))
                |(?P<two>
                  (?P<two_day>3[01]|[12]\d|0[1-9]|\d)
                  (?P<two_sep>[-\.\/\s])
                  (?P<two_mnth>0[1-9]|1[012]|\d)
                  (?P=two_sep)
                  (?P<two_yr>[1-9]\d))
                (?:\s*)
            """, re.VERBOSE)
            m = datere.match(dt)
            if not m:
                raise ValueError("Cannot parse %r as date." % dt)

            g = m.groupdict()
            for p in ['iso', 'dmy', 'nsp', 'isonsp', 'two']:
                if g[p]:
                    prefix = p

            day, month, year = [int(g['%s_%s' % (prefix, val)])
                                for val in ['day', 'mnth', 'yr']]

            if year < 13:
                raise ValueError("Cannot parse %r as date." % dt)
            if year < 100:
                year += 2000

            self.datetime = datetime(year, month, day)

    def __eq__(self, other):
        return self.__str__() == other.__str__()

    def __ne__(self, other):
        return self.__str__() != other.__str__()

    def next(self, n=1):
        return self.shift(n)

    def prev(self, n=1):
        return self.shift(-n)

    def clone(self):
        return self.__class__(self.datetime)

    def format(self, format_string):
        return self.datetime.strftime(format_string)

    def range(self, format=None):
        return [self.start(format), self.end(format)]

    def __str__(self):
        return self.datetime.strftime('%d.%m.%Y')

    def __repr__(self):
        return "%s: %s" % (self.__class__.__name__, self.__str__())


class Year(Period):
    @property
    def year(self):
        return self.datetime.year

    def start(self, format=None):
        d = datetime(self.year, 1, 1)
        return d.strftime(format) if format else d

    def end(self, format=None):
        d = datetime(self.year, 12, 31, 23, 59, 59, 999999)
        return d.strftime(format) if format else d

    def shift(self, n):
        self.datetime += relativedelta(years=n)
        return self

    def __str__(self):
        return self.datetime.strftime('%Y')


class Quarter(Year):
    @property
    def quarter(self):
        return self.datetime.month // 4 + 1

    def start(self, format=None):
        d = datetime(self.year, self.quarter*3-2, 1)
        return d.strftime(format) if format else d

    def end(self, format=None):
        d = datetime(self.year, self.quarter * 3, calendar.monthrange(self.year, self.quarter * 3)[1], 23, 59, 59, 999999)
        return d.strftime(format) if format else d

    def shift(self, n):
        self.datetime += relativedelta(months=n*3)
        return self

    def __str__(self):
        return self.datetime.strftime('Q%s.%%Y' % self.quarter)


class Month(Quarter):
    @property
    def month(self):
        return self.datetime.month

    def start(self, format=None):
        d = datetime(self.year, self.month, 1)
        return d.strftime(format) if format else d

    def end(self, format=None):
        d = datetime(self.year, self.month, calendar.monthrange(self.year, self.month)[1], 23, 59, 59,
                     999999)
        return d.strftime(format) if format else d

    def shift(self, n):
        self.datetime += relativedelta(months=n)
        return self

    def __str__(self):
        return self.datetime.strftime('%m.%Y')


class Week(Month):
    @property
    def week(self):
        return self.datetime.isocalendar()[1]

    def start(self, format=None):
        delta = relativedelta(days=self.datetime.weekday())
        d = self.datetime - delta
        d = datetime(d.year, d.month, d.day)
        return d.strftime(format) if format else d

    def end(self, format=None):
        delta = relativedelta(days=6-self.datetime.weekday())
        d = self.datetime + delta
        d = datetime(d.year, d.month, d.day, 23, 59, 59, 999999)
        return d.strftime(format) if format else d

    def shift(self, n):
        self.datetime += relativedelta(weeks=n)
        return self

    def __str__(self):
        return self.datetime.strftime('W%s.%%Y' % self.week)


class Day(Week):
    @property
    def day(self):
        return self.datetime.day

    @property
    def weekday(self):
        return self.datetime.weekday()+1

    def start(self, format=None):
        d = datetime(self.datetime.year, self.datetime.month, self.datetime.day)
        return d.strftime(format) if format else d

    def end(self, format=None):
        d = datetime(self.datetime.year, self.datetime.month, self.datetime.day, 23, 59, 59, 999999)
        return d.strftime(format) if format else d

    def shift(self, n):
        self.datetime += relativedelta(days=n)
        return self

    def __str__(self):
        return self.datetime.strftime('%d.%m.%Y')


if __name__ == "__main__":
    import doctest
    doctest.testmod()