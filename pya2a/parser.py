import os
from lxml import etree

import A2A

#from pya2a import NAMESPACE
NAMESPACE = {"a2a": "http://Mindbus.nl/A2A"}


class Document:

    NS = NAMESPACE

    def __init__(self, path=None):

        if os.path.exists(path):
            self.tree = etree.parse(path)

            self.parse()

    def fromString(self, text):
        pass

    def fromTree(self, tree):
        self.tree = tree

        self.parse()

    def parse(self):

        if not self.tree:
            print("error")

        self._parsePersons()
        # self._parseEvents()
        # self._parseObjects()
        # self._parseSource()
        # self._parseRelations()

        return self

    def _parsePersons(self):

        elements = self.tree.findall('//a2a:Person', namespaces=self.NS)
        self.persons = [A2A.Person(el)
                        for el in elements]  # or should this be a generator?

    def _parseEvents(self):

        elements = self.tree.findall('//a2a:Event', namespaces=self.NS)
        self.events = [A2A.Event(el)
                       for el in elements]  # or should this be a generator?

    def _parseObjects(self):

        elements = self.tree.findall('//a2a:Object', namespaces=self.NS)
        self.objects = [A2A.Object(el)
                        for el in elements]  # or should this be a generator?

    def _parseSource(self):
        self.source = A2A.Source(
            self.tree.find('//a2a:Source', namespaces=self.NS))

    def _parseRelations(self):
        elements = self.tree.xpath(
            "a2a:A2A/*[starts-with(name(), 'a2a:Relation')]",
            namespaces=self.NS)
        self.relations = [A2A.Relation(el) for el in elements]
        pass


if __name__ == "__main__":
    d = Document(
        '/home/leon/Documents/Golden_Agents/A2A/pya2a/pya2a/test/NL-UtHUA_A338180_000021.a2a.xml'
    )

    print(d.persons)
