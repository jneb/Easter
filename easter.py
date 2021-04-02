#!python3
"""Program for calculating Good Friday and Easter for any given year between
1900 and 2100.
For Hanna's birthday, 2 april 2021.
Using anonymous algorithm; see https://en.wikipedia.org/wiki/Computus
"""

import argparse, datetime

def days(n):
    return datetime.timedelta(days=n)

def easter(Y):
    """The actual computation
    >>> easter(1961)
    datetime.date(1961, 4, 2)
    >>> easter(2021)
    datetime.date(2021, 4, 4)
    """
    a = Y % 19
    b, c = divmod(Y, 100)
    d = b // 4
    e = b % 4
    f = (b + 8) // 25
    g = (b - f + 1) //3
    h = (19 * a + b - d - g + 15) % 30
    i, k = divmod(c, 4)
    l = (32 + 2 * e + 2 * i - h - k) % 7
    m = (a + 11 * h + 22 * l) // 451
    month, day = divmod(h + l - 7 * m + 114, 31)
    return datetime.date(Y, month, day + 1)

def hanna():
    """Find dates from 1999 on where Good Friday is on April 2nd.
    >>> hanna()
    1999
    2010
    2021
    2083
    2094
    """
    for y in range(1999, 2100):
        if easter(y) == datetime.date(y, 4, 4): print(y)

def main(args):
    """Main program
    """
    Y = args.year or datetime.date.today().year
    if Y < 100: Y += 2000
    d = easter(Y)
    print(f"Easter day for year {Y}: {d:%d %B}")
    print(f"Good friday: {d-days(2):%d %B}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description='Calculate good friday for a given year')
    parser.add_argument('year', metavar='Y', type=int, nargs='?',
        help='Year for which to calculate the good friday date')
    parser.add_argument('-t', '--test', action='store_true',
        help='Self test')
    parser.add_argument('--hanna', action='store_true',
        help='argparse.suppress')
    args = parser.parse_args()
    if args.test:
        import doctest
        doctest.testmod()
    elif args.hanna:
        hanna()
    else:
        main(args)
