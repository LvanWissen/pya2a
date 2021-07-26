import datetime
import dateutil.parser

import lxml.etree

from pya2a.utils import parseRemark


class Entity:
    NAMESPACE = {"a2a": "http://Mindbus.nl/A2A"}


class Person(Entity):
    """

    """
    def __init__(self, element: lxml.etree._Element):

        self.id = element.attrib['pid']
        self.relations = []

        ## PersonName
        pn = element.find('a2a:PersonName', namespaces=self.NAMESPACE)
        self.PersonName = PersonName(pn)

        # Gender
        if (el := element.find('a2a:Gender',
                               namespaces=self.NAMESPACE)) is not None:
            self.Gender = el.text

        # Residence
        if (el := element.find('a2a:Residence',
                               namespaces=self.NAMESPACE)) is not None:
            self.Residence = Place(el)

        # Religion
        if (el := element.find('a2a:Religion',
                               namespaces=self.NAMESPACE)) is not None:
            self.Religion = el.find('a2a:ReligionLiteral',
                                    namespaces=self.NAMESPACE).text

        # Origin
        if (el := element.find('a2a:Origin',
                               namespaces=self.NAMESPACE)) is not None:
            self.Origin = Place(el)

        # Age

        # BirthDate
        if (el := element.find('a2a:BirthDate',
                               namespaces=self.NAMESPACE)) is not None:
            self.BirthDate = Date(el)

        # BirthPlace
        if (el := element.find('a2a:BirthPlace',
                               namespaces=self.NAMESPACE)) is not None:
            self.BirthPlace = Place(el)

        # Profession
        if (el := element.find('a2a:Profession',
                               namespaces=self.NAMESPACE)) is not None:
            self.Profession = el.text

        # MaritalStatus
        if (el := element.find('a2a:MaritalStatus',
                               namespaces=self.NAMESPACE)) is not None:
            self.Gender = el.text

        # PersonRemark
        if (els := element.findall('a2a:PersonRemark',
                                   namespaces=self.NAMESPACE)) is not None:
            remarks = []
            for el in els:
                remarkType = el.attrib['Key']
                remark = el.find('a2a:Value', namespaces=self.NAMESPACE).text

                remarks.append((remarkType, parseRemark(remark)))
            self.Remarks = dict(remarks)

    def __getattr__(self, attr):
        return None


class PersonName(Entity):
    """
    A2A:PersonNameAlias, A2A:PersonNameFamilyName, A2A:PersonNameFirstName,
    A2A:PersonNameInitials, A2A:PersonNameLastName, A2A:PersonNameLiteral,
    A2A:PersonNameNickName, A2A:PersonNamePatronym, A2A:PersonNamePrefixLastName,
    A2A:PersonNameRemark, A2A:PersonNameTitle, A2A:PersonNameTitleOfNobility
    """
    def __init__(self, element: lxml.etree._Element):

        for child in element.getchildren():
            key = child.tag.replace(f"{{{self.NAMESPACE['a2a']}}}", '')
            value = child.text

            self.__setattr__(key, value)

    def __iter__(self):
        for i in vars(self):
            if i.startswith('PersonName'):
                yield self.__getattribute__(i)
            else:
                continue

    def __getattr__(self, attr):
        return None


class Event(Entity):
    def __init__(self, element: lxml.etree._Element):
        self.id = element.attrib['eid']
        self.relations = []

        # EventType
        self.EventType = element.find('a2a:EventType',
                                      namespaces=self.NAMESPACE).text

        # EventDate
        if (el := element.find('a2a:EventDate',
                               namespaces=self.NAMESPACE)) is not None:
            self.EventDate = Date(el)

        # EventPlace
        if (el := element.find('a2a:EventPlace',
                               namespaces=self.NAMESPACE)) is not None:
            self.EventPlace = Place(el)

        # EventReligion
        if (el := element.find('a2a:EventReligion',
                               namespaces=self.NAMESPACE)) is not None:
            self.EventReligion = el.find('a2a:ReligionLiteral',
                                         namespaces=self.NAMESPACE).text

        # EventRemark
        if (els := element.findall('a2a:EventRemark',
                                   namespaces=self.NAMESPACE)) is not None:
            remarks = []
            for el in els:
                remarkType = el.attrib['Key']
                remark = el.find('a2a:Value', namespaces=self.NAMESPACE).text

                remarks.append((remarkType, parseRemark(remark)))
            self.Remarks = dict(remarks)

    def __getattr__(self, attr):
        return None


class Object(Entity):
    def __init__(self, element: lxml.etree._Element):
        self.id = element.attrib['oid']
        self.relations = []


class Source(Entity):
    """
    A2A:EAC, A2A:EAD, A2A:RecordGUID, A2A:RecordIdentifier, A2A:SourceAvailableScans, A2A:SourceDate,
    A2A:SourceDigitalOriginal, A2A:SourceDigitalizationDate, A2A:SourceIndexDate, A2A:SourceLastChangeDate,
    A2A:SourcePlace, A2A:SourceReference, A2A:SourceRemark, A2A:SourceType
    """
    def __init__(self, element: lxml.etree._Element):

        # SourcePlace
        self.SourcePlace = Place(
            element.find('a2a:SourcePlace', namespaces=self.NAMESPACE))

        # SourceIndexDate
        date_from = element.find('a2a:SourceIndexDate/a2a:From',
                                 namespaces=self.NAMESPACE).text
        self.IndexDateFrom = dateutil.parser.parse(date_from)

        date_to = element.find('a2a:SourceIndexDate/a2a:To',
                               namespaces=self.NAMESPACE).text
        self.IndexDateTo = dateutil.parser.parse(date_to)

        # SourceDate
        if (el := element.find('a2a:SourceDate',
                               namespaces=self.NAMESPACE)) is not None:
            self.SourceDate = Date(el)

        # SourceType
        self.SourceType = element.find('a2a:SourceType',
                                       namespaces=self.NAMESPACE).text

        # EAD

        # EAC

        # SourceReference
        self.SourceReference = SourceReference(
            element.find('a2a:SourceReference', namespaces=self.NAMESPACE))

        # SourceAvailableScans
        if (el := element.find('a2a:SourceAvailableScans',
                               namespaces=self.NAMESPACE)) is not None:
            self.scans = [
                Scan(i)
                for i in el.findall('a2a:Scan', namespaces=self.NAMESPACE)
            ]
        else:
            self.scans = []

        # SourceDigitalizationDate
        if (el := element.find('a2a:SourceDigitalizationDate',
                               namespaces=self.NAMESPACE)) is not None:
            self.SourceDigitalizationDate = datetime.date.fromisoformat(
                el.text)

        # SourceLastChangeDate
        self.SourceLastChangeDate = datetime.date.fromisoformat(
            element.find('a2a:SourceLastChangeDate',
                         namespaces=self.NAMESPACE).text)

        # SourceRetrievalDate
        if (el := element.find('a2a:SourceRetrievalDate',
                               namespaces=self.NAMESPACE)) is not None:
            self.SourceRetrievalDate = datetime.date.fromisoformat(el.text)

        # SourceDigitalOriginal

        # RecordIdentifier
        if (el := element.find('a2a:RecordIdentifier',
                               namespaces=self.NAMESPACE)) is not None:
            self.identifier = el.text

        # RecordGUID
        guid = element.find('a2a:RecordGUID', namespaces=self.NAMESPACE).text
        self.guid = guid.replace('{', '').replace('}', '')  # m$

        # SourceRemark
        if (els := element.findall('a2a:SourceRemark',
                                   namespaces=self.NAMESPACE)) is not None:
            remarks = []
            for el in els:
                remarkType = el.attrib['Key']
                remark = el.find('a2a:Value', namespaces=self.NAMESPACE).text

                remarks.append((remarkType, parseRemark(remark)))

            remarkKeys = [i[0] for i in remarks]
            duplicateKeys = set(k for k in remarkKeys
                                if remarkKeys.count(k) > 1)
            duplicateKeys.add('filename')  # hardcode

            remarkDict = dict(
                [i for i in remarks if i[0] not in duplicateKeys])

            # add the duplicate keys with list value
            for key in duplicateKeys:
                remarkDict[key] = [
                    i[1]['Other'] for i in remarks if i[0] == key
                ]

            self.Remarks = remarkDict


class Relation(Entity):
    def __init__(self, element: lxml.etree._Element):

        self.RelationType = element.find('a2a:RelationType',
                                         namespaces=self.NAMESPACE).text

        # ExtendedRelationType
        if (el := element.find('a2a:ExtendedRelationType',
                               namespaces=self.NAMESPACE)) is not None:
            self.ExtendedRelationType = el.text

    def __get__(self, value):
        return self.value


class RelationEP(Relation):
    def __init__(self, element: lxml.etree._Element):
        super().__init__(element)

        self.person = element.find('a2a:PersonKeyRef',
                                   namespaces=self.NAMESPACE).text
        self.event = element.find('a2a:EventKeyRef',
                                  namespaces=self.NAMESPACE).text


class RelationPP(Relation):
    def __init__(self, element: lxml.etree._Element):
        super().__init__(element)

        self.persons = [
            i.text for i in element.findall('a2a:PersonKeyRef',
                                            namespaces=self.NAMESPACE)
        ]


class RelationPO(Relation):
    def __init__(self, element: lxml.etree._Element):
        super().__init__(element)

        self.person = element.find('a2a:PersonKeyRef',
                                   namespaces=self.NAMESPACE).text
        self.object = element.find('a2a:ObjectKeyRef',
                                   namespaces=self.NAMESPACE).text


class RelationP(Relation):
    def __init__(self, element: lxml.etree._Element):
        super().__init__(element)

        self.person = element.find('a2a:PersonKeyRef',
                                   namespaces=self.NAMESPACE).text


class RelationOO(Relation):
    def __init__(self, element: lxml.etree._Element):
        super().__init__(element)

        self.objects = [
            i.text for i in element.findall('a2a:ObjectKeyRef',
                                            namespaces=self.NAMESPACE)
        ]


class RelationO(Relation):
    def __init__(self, element: lxml.etree._Element):
        super().__init__(element)

        self.object = element.find('a2a:ObjectKeyRef',
                                   namespaces=self.NAMESPACE).text


class Place(Entity):
    """
    A2A:Block, A2A:Country, A2A:County, A2A:DescriptiveLocationIndicator, A2A:DetailPlaceRemark,
    A2A:HouseName, A2A:HouseNumber, A2A:HouseNumberAddition, A2A:Latitude, A2A:Longitude,
    A2A:Municipality, A2A:PartMunicipality, A2A:Place, A2A:Province, A2A:Quarter, A2A:State, A2A:Street
    """
    def __init__(self, element: lxml.etree._Element):

        for child in element.getchildren():
            key = child.tag.replace(f"{{{self.NAMESPACE['a2a']}}}", '')
            value = child.text

            self.__setattr__(key, value)


class SourceReference(Entity):
    def __init__(self, element: lxml.etree._Element):

        for child in element.getchildren():
            key = child.tag.replace(f"{{{self.NAMESPACE['a2a']}}}", '')
            value = child.text

            self.__setattr__(key, value)


class Scan(Entity):
    def __init__(self, element: lxml.etree._Element):

        for child in element.getchildren():
            key = child.tag.replace(f"{{{self.NAMESPACE['a2a']}}}", '')
            value = child.text

            self.__setattr__(key, value)


class Date(Entity):
    def __init__(self, element: lxml.etree._Element):

        # Calendar="" IndexDateTime=""
        if 'Calendar' in element.attrib:
            self.calendar = element.attrib['Calendar']
        if 'IndexDateTime' in element.attrib:
            self.IndexDateTime = element.attrib['IndexDateTime']

        for child in element.getchildren():
            key = child.tag.replace(f"{{{self.NAMESPACE['a2a']}}}", '')
            value = child.text

            self.__setattr__(key, value)

        self.date = self._toISO()

    def _toISO(self):

        arguments = {
            k.lower(): int(v)
            for k, v in vars(self).items()
            if k.lower() in ('year', 'month', 'day', 'hour', 'minute')
        }

        if {'year', 'month', 'day', 'hour'}.issubset(arguments):

            date = datetime.datetime(**arguments)

            #return date.isoformat()
            return date

        elif {'year', 'month', 'day'}.issubset(arguments):

            date = datetime.date(**arguments)

            #return date.isoformat()
            return date

        elif {'year', 'month'}.issubset(arguments):
            return f"{arguments['year']}-{arguments['month']}"

        elif {'year'}.issubset(arguments):
            return f"{arguments['year']}"

        else:
            return None

    def __str__(self):
        return self._toISO()
