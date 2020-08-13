from datetime import date

import lxml.etree

from utils import parseRemark


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
            self.Religion = el.text

        # Origin
        if (el := element.find('a2a:Origin',
                               namespaces=self.NAMESPACE)) is not None:
            self.Origin = Place(el)

        # Age

        # BirthDate

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
            self.Remarks = dict(remarks)  # This only works if 'Key' is unique


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


class Event(Entity):
    def __init__(self, element: lxml.etree._Element):
        self.id = element.attrib['eid']
        self.relations = []

        # EventType
        self.EventType = element.find('a2a:EventType',
                                      namespaces=self.NAMESPACE).text

        # EventDate

        # EventPlace
        if (el := element.find('a2a:EventPlace',
                               namespaces=self.NAMESPACE)) is not None:
            self.EventPlace = Place(el)

        # EventReligion

        # EventRemark
        if (els := element.findall('a2a:EventRemark',
                                   namespaces=self.NAMESPACE)) is not None:
            remarks = []
            for el in els:
                remarkType = el.attrib['Key']
                remark = el.find('a2a:Value', namespaces=self.NAMESPACE).text

                remarks.append((remarkType, parseRemark(remark)))
            self.Remarks = dict(remarks)


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
        self.IndexDateFrom = element.find('a2a:SourceIndexDate/a2a:From',
                                          namespaces=self.NAMESPACE).text
        self.IndexDateTo = element.find('a2a:SourceIndexDate/a2a:To',
                                        namespaces=self.NAMESPACE).text

        # SourceDate

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
                Scan(i) for i in element.findall('a2a:SourceAvailableScans',
                                                 namespaces=self.NAMESPACE)
            ]

        # SourceDigitalizationDate
        if (el := element.find('a2a:SourceDigitalizationDate',
                               namespaces=self.NAMESPACE)) is not None:
            self.SourceDigitalizationDate = date.fromisoformat(el.text)

        # SourceLastChangeDate
        self.SourceLastChangeDate = date.fromisoformat(
            element.find('a2a:SourceLastChangeDate',
                         namespaces=self.NAMESPACE).text)

        # SourceRetrievalDate
        if (el := element.find('a2a:SourceRetrievalDate',
                               namespaces=self.NAMESPACE)) is not None:
            self.SourceRetrievalDate = date.fromisoformat(el.text)

        # SourceDigitalOriginal

        # RecordIdentifier
        if (el := element.find('a2a:RecordIdentifier',
                               namespaces=self.NAMESPACE)) is not None:
            self.identifier = el.text

        # RecordGUID
        self.guid = element.find('a2a:RecordGUID',
                                 namespaces=self.NAMESPACE).text

        # SourceRemark
        if (els := element.findall('a2a:SourceRemark',
                                   namespaces=self.NAMESPACE)) is not None:
            remarks = []
            for el in els:
                remarkType = el.attrib['Key']
                remark = el.find('a2a:Value', namespaces=self.NAMESPACE).text

                remarks.append((remarkType, parseRemark(remark)))
            self.Remarks = dict(remarks)


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

        for child in element.getchildren():
            key = child.tag.replace(f"{{{self.NAMESPACE['a2a']}}}", '')
            value = child.text

            self.__setattr__(key, value)