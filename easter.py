#!python3
"""Program for calculating Good Friday and Easter for any given year between
1900 and 2100.
For Hanna's birthday, 2 april 2021.
Using New Scientist algorithm; see https://en.wikipedia.org/wiki/Computus
"""

import argparse
from datetime import timedelta, date

def easter(Y):
    """The actual computation
    >>> easter(1961)
    datetime.date(1961, 4, 2)
    >>> easter(2021)
    datetime.date(2021, 4, 4)
    """
    # write year as 400d + 100e + 4i + k
    b, c = divmod(Y, 100)
    d, e = divmod(b, 4)
    i, k = divmod(c, 4)
    # slow shift over centuries: 6 for 1900-2100
    g = (8 * b + 13) // 25
    # 19 year moon cycle
    a = Y % 19
    # Probably nobody knows what's going on here
    h = (19 * a + b - d - g + 15) % 30
    l = (32 + 2 * e + 2 * i - h - k) % 7
    m = (a + 11 * h + 19 * l) // 433
    month = (h + l - 7 * m + 90) // 25
    day = (h + l - 7 * m + 33 * month + 19) % 32
    return date(Y, month, day)

def on(mmdd='404'):
    """Print years between 1964 and 2150 where eastern fall on a given date.
    First digit of month may be omitted
    >>> on()
    Years: 1999, 2010, 2021, 2083, 2094
    """
    mm, dd = int(mmdd[:-2]), int(mmdd[-2:])
    years = [y for y in range(1964, 2150) if easter(y) == date(y, mm, dd)]
    if years:
        print("Years:", ', '.join(map(str, years)))
    else:
        print("No year has easter on this month and day.")

def main(year, verbose=False):
    """Main program
    >>> main(1999)
    Easter day for year 1999: 04 April
    Good friday: 02 April
    """
    Y = year or date.today().year
    if Y < 100: Y += 2000
    d = easter(Y)
    print(f"Easter day for year {Y}: {d:%d %B}")
    related = [
        (-46, "Ash Wednesday"),
        (-3, "Maundy Thursday"),
        (-2, "Good friday"),
        (-1, "Holy Saturday"),
        (39, "Ascension"),
        (49, "Pentecost"),
        ]
    if not verbose:
        related = related[2:3]
    for delta, name in related:
        print(f"{name}: {d+timedelta(days=delta):%d %B}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description='Calculate good friday for a given year')
    parser.add_argument('year', metavar='Y', type=int, nargs='?',
        help='year for which to calculate the good friday date')
    parser.add_argument('-v', '--verbose', action='store_true',
        help='show all related Christian calendar days')
    parser.add_argument('-t', '--test', action='store_true',
        help='self test')
    parser.add_argument('-o', '--on', nargs='?', metavar='MMDD',
        const='0404',
        help='print years where easter falls on a given date')
    args = parser.parse_args()
    if args.test:
        import doctest
        doctest.testmod()
    elif args.on:
        try: on(args.on)
        except ValueError:
            parser.error('Invalid month & day specifier: ' + args.on)
    else:
        main(args.year, args.verbose)
