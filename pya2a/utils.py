import re
from collections import defaultdict, Counter


def parseRemark(remark: str):

    parsedRemarks = remarkParser(remark)

    if len(parsedRemarks) == 1 and parsedRemarks[0][0] == 'Other':
        return parsedRemarks[0][1]
    else:

        return defaultdictify(parsedRemarks)


def defaultdictify(d):

    if type(d) == list:
        data = defaultdict(list)

        keys, _ = zip(*d)
        keyCounts = Counter(keys)

        for key, value in d:

            if keyCounts[key] == 1:
                data[key] = value
            else:
                data[key].append(value)

        d = data

    if type(d) == dict:
        return {k: defaultdictify(v) for k, v in d.items()}
    else:
        return d


def remarkParser(remark: str):

    remark = remark.strip()

    fields = re.split(r'\n|; ', remark)

    parsedRemarks = []
    for f in fields:
        if ': ' in f:
            _, key, _, value = re.split(r'(^.*?)(: )', f)

            if ': ' in value:
                value = remarkParser(value)

            f = (key, value)
        else:
            f = ('Other', f)

        parsedRemarks.append(f)

    return parsedRemarks