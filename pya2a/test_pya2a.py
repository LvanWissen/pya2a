import datetime

from . import DocumentCollection, Document

# run from tldr
OTR = 'pya2a/test/saa_01cbd894-13ac-4799-b864-e3f4cba76f17.xml'


def test_parser_otr(document=OTR):
    d = Document(document)

    # guid
    assert d.source.guid == '01cbd894-13ac-4799-b864-e3f4cba76f17'

    # date
    assert d.source.IndexDateFrom == datetime.datetime(1655, 6, 10, 0, 0)
    assert d.source.IndexDateTo == datetime.datetime(1655, 6, 10, 0, 0)

    # persons
    assert len(d.persons) == 2
    assert d.persons[0].id == 'Person:961f6b15-e7fc-53f7-e053-b784100aa83b'