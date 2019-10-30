import lxml

class Person:
    def __init__(self, element: lxml.etree._Element):
        print(element)


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
