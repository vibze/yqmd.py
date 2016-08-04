# YQMD
A set of classes to work with common period units: `Year`, `Quarter`, `Month`, `Week`, `Day`

#### Installation
```
pip install yqmd
```

### Usage examples

#### Create a sequence

```python
>>> Quarter.sequence('01.01.2014', '01.01.2015')
[Quarter: Q1.2014, Quarter: Q2.2014, Quarter: Q2.2014, Quarter: Q3.2014, Quarter: Q1.2015]
>>> Day.sequence(datetime(2015, 1, 29), datetime(2015, 2, 2))
[Day: 29.01.2015, Day: 30.01.2015, Day: 31.01.2015, Day: 01.02.2015, Day: 02.02.2015]
>>> Month.sequence(20150505, 20141201)
[Month: 05.2015, Month: 04.2015, Month: 03.2015, Month: 02.2015, Month: 01.2015, Month: 12.2014]
```

#### Parse string

```python
>>> Month.parse('01 12 2014', '%d %m %Y')
Month: 12.2014
```

#### Instantiate using datetime instance

```python
>>> Year(datetime(2015, 1, 15))
Year: 2015
```

#### You can get current period without passing any parameters

```python
>>> Month()
Month: 05.2015
```

#### Instantiate using another Period instance

```python
>>> m = Month('01-01-2016')
>>> Month(m)
Month: 01.2016
```

#### Instantiate with string

```python
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
```

#### Shifting

```python
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
```

#### Cloning

```python
>>> month = Month('05.05.1985')
>>> month
Month: 05.1985
>>> month.next()
Month: 06.1985
>>> month.clone().next(5)
Month: 11.1985
>>> month
Month: 06.1985
```

#### Formatting period representation

```python
>>> month = Month('05.05.1985')
>>> month.format('%Y%m')
'198505'
```

#### Gettings start/end of period
```python
>>> quarter = Quarter(20150606)
>>> quarter
Quarter: Q2.2015
>>> quarter.start('%d.%m.%Y')
'01.04.2015'
>>> quarter.end()
datetime.datetime(2015, 6, 30, 23, 59, 59, 999999)
>>> quarter.range('%d-%m-%Y')
['01-04-2015', '30-06-2015']
```

Periods also have numeric attributes representing year/quarter/month/week/day if it's possible.
For example year only has `year` attribute and month has `year`, `quarter` and `month` attributes.

#### Various database shortcuts
```python
>>> Month('05.05.1985').as_oracle_date
"TO_DATE('19850505', 'yyyymmdd')"

>>> Month('05.05.1985').as_mysql_date
'1985-05-05'
```
