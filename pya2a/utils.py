import re
from collections import defaultdict, Counter


def parseRemark(remark: str):

    items = []

    lines = [i.strip() for i in remark.split('\n')]
    for line in lines:
        if ': ' in line:
            key, values = line.split(': ', 1)

            if ': ' in values and key in ('Positie op scan', ):  # any more?
                values = [
                    tuple(i.strip().split(': ', 1)) for i in values.split('; ')
                ]
                print(values)
                values = dict(values)

            items.append((key, values))
        elif line:
            items.append(('Other', line))

    data = defaultdict(list)
    for k, v in items:
        data[k].append(v)

    for k, v in data.items():
        if len(v) == 1:
            data[k] = data[k][0]

    return data