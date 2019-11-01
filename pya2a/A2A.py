import lxml


class Entity:
    NAMESPACE = {"a2a": "http://Mindbus.nl/A2A"}


class Person(Entity):
    """

    """
    def __init__(self, element: lxml.etree._Element):

        ## PersonName
        pn = element.find('a2a:PersonName', namespaces=self.NAMESPACE)
        self.PersonName = PersonName(pn)

        # Gender
        if element.find('a2a:Gender', namespaces=self.NAMESPACE):
            self.Gender = element.find('a2a:Gender',
                                       namespaces=self.NAMESPACE).text

        # Residence

        # Religion

        # Origin

        # Age

        # BirthDate

        # BirthPlace

        # Profession

        # MaritalStatus
        if element.find('a2a:MaritalStatus', namespaces=self.NAMESPACE):
            self.Gender = element.find('a2a:Gender',
                                       namespaces=self.NAMESPACE).text

        # PersonRemark


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


class Event:
    def __init__(self, element: lxml.etree._Element):
        print(element)


class Object:
    def __init__(self, element: lxml.etree._Element):
        print(element)


class Source:
    def __init__(self, element: lxml.etree._Element):
        print(element)


class Relation:
    def __init__(self, element: lxml.etree._Element):
        print(element)


class RelationEP(Relation):
    def __init__(self, element: lxml.etree._Element):
        print(element)


class RelationPP(Relation):
    def __init__(self, element: lxml.etree._Element):
        print(element)


class RelationPO(Relation):
    def __init__(self, element: lxml.etree._Element):
        print(element)


class RelationP(Relation):
    def __init__(self, element: lxml.etree._Element):
        print(element)


class RelationOO(Relation):
    def __init__(self, element: lxml.etree._Element):
        print(element)


class RelationO(Relation):
    def __init__(self, element: lxml.etree._Element):
        print(element)
