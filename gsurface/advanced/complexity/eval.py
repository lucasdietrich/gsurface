import re

rec = re.compile(r"^((iM(?P<imodel>\d+))|(?P<model>M))-(F(?P<force>\d+)(I(?P<interaction>\d+))?)-(T(?P<time>\d+))$")

rprs = [
    'iM62-F12I324-T10000',
    'M-F12-T100',
    'iM62-F12I324-T10000'
]

for rpr in rprs:
    m = rec.match(rpr)

    if m:
        print(m.groupdict())
