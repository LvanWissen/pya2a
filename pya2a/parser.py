import os
from collections import defaultdict

from lxml import etree

import A2A

#from pya2a import NAMESPACE
NAMESPACE = {"a2a": "http://Mindbus.nl/A2A"}


class Document:

    NS = NAMESPACE

    def __init__(self, path=None):

        self.references = defaultdict(dict)

        if os.path.exists(path):
            self._tree = etree.parse(path)

            self.parse()

    def __iter__(self):
        for i in self.getEntities():
            yield i

    def fromString(self, text):
        pass

    def fromTree(self, tree):
        self._tree = tree

        self.parse()

    def parse(self):

        if not self._tree:
            print("error")

        self._parsePersons()
        self._parseEvents()
        self._parseObjects()
        self._parseSource()
        self._parseRelations()

        return self

    def _parsePersons(self):

        elements = self._tree.findall('//a2a:Person', namespaces=self.NS)
        self.persons = [A2A.Person(el)
                        for el in elements]  # or should this be a generator?

        for p in self.persons:
            self.references['person'][p.id] = p

    def _parseEvents(self):

        elements = self._tree.findall('//a2a:Event', namespaces=self.NS)
        self.events = [A2A.Event(el)
                       for el in elements]  # or should this be a generator?

        for e in self.events:
            self.references['event'][e.id] = e

    def _parseObjects(self):

        elements = self._tree.findall('//a2a:Object', namespaces=self.NS)
        self.objects = [A2A.Object(el)
                        for el in elements]  # or should this be a generator?

        for o in self.objects:
            self.references['object'][o.id] = o

    def _parseSource(self):
        self.source = A2A.Source(
            self._tree.find('//a2a:Source', namespaces=self.NS))

    def _parseRelations(self):
        """
        Relation factory.
        """

        elements = self._tree.xpath(
            "a2a:A2A/*[starts-with(name(), 'a2a:Relation')]",
            namespaces=self.NS)

        relations = []
        for el in elements:
            if 'RelationEP' in el.tag:
                relation = A2A.RelationEP(el)
            elif 'RelationPP' in el.tag:
                relation = A2A.RelationPP(el)
            elif 'RelationPO' in el.tag:
                relation = A2A.RelationPO(el)
            elif 'RelationEO' in el.tag:
                relation = A2A.RelationEO(el)
            elif 'RelationP' in el.tag:
                relation = A2A.RelationP(el)
            elif 'RelationOO' in el.tag:
                relation = A2A.RelationOO(el)
            elif 'RelationO' in el.tag:
                relation = A2A.RelationO(el)

            # And make references to instantiated objects
            if hasattr(relation, 'person'):
                relation.person = self.references['person'][relation.person]
            if hasattr(relation, 'event'):
                relation.event = self.references['event'][relation.event]
            if hasattr(relation, 'object'):
                relation.object = self.references['object'][relation.object]
            if hasattr(relation, 'persons'):
                relation.objects = tuple(
                    self.references['person'][relation.persons[0]],
                    self.references['person'][relation.persons[1]])
            if hasattr(relation, 'objects'):
                relation.objects = tuple(
                    self.references['object'][relation.objects[0]],
                    self.references['object'][relation.objects[1]])

            relations.append(relation)

        self.relations = relations

    def getEntities(self):

        return self.persons + self.events + self.objects + \
            self.relations + [self.source]


if __name__ == "__main__":
    d = Document(
        '/home/leon/Documents/Golden_Agents/A2A/pya2a/pya2a/test/NL-UtHUA_A338180_000021.a2a.xml'
    )

    for i in d:
        print(vars(i))
        print()
