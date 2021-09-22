import os
import errno
import xml.etree.ElementTree as ET

import pya2a.models as models

#from pya2a import NAMESPACE
NAMESPACE = {"a2a": "http://Mindbus.nl/A2A"}


class DocumentCollection:

    NS = NAMESPACE

    def __init__(self, path=None, treeElement=None):

        self.documents = []

        if path and os.path.exists(path) and not os.path.isdir(path):
            self._tree = ET.parse(path)
        elif treeElement is not None:
            self._tree = treeElement
        else:
            print("PATH", path)
            raise OSError

        records = self._tree.findall('.//a2a:A2A', namespaces=self.NS)
        if (nRecords := len(records)) == 1:
            #TODO: warning/error?
            self.__class__ = Document
            self.__init__(treeElement=records[0])
        elif nRecords > 1:
            for r in records:
                d = Document(treeElement=r)
                self.documents.append(d)

    def __iter__(self):
        for i in self.documents:
            yield i


class Document:

    NS = NAMESPACE

    def __init__(self, path=None, treeElement=None):

        self._refs = {'person': {}, 'event': {}, 'object': {}}

        if path and os.path.exists(path) and not os.path.isdir(path):
            self._tree = ET.parse(path)

            records = self._tree.findall('.//a2a:A2A', namespaces=self.NS)
            if (nRecords := len(records)) > 1:
                #TODO: warning/error?
                self.__class__ = DocumentCollection
                self.__init__(treeElement=self._tree)
            elif nRecords == 1:
                self._elem = records[0]
                self.parse()

        elif treeElement is not None:
            self._elem = treeElement
            self.parse()

        else:
            raise FileNotFoundError(errno.ENOENT, os.strerror(errno.ENOENT),
                                    path)

    def __iter__(self):
        for i in self.getEntities():
            yield i

    def fromString(self, text):
        pass

    def fromTree(self, tree):
        self._tree = tree

        self.parse()

    def parse(self):

        if self._elem is None:
            print("error")

        self._parsePersons()
        self._parseEvents()
        self._parseObjects()
        self._parseSource()
        self._parseRelations()

        return self

    def _parsePersons(self):

        elements = self._elem.findall('.//a2a:Person', namespaces=self.NS)
        self.persons = [models.Person(el)
                        for el in elements]  # or should this be a generator?

        for p in self.persons:
            self._refs['person'][p.id] = p

    def _parseEvents(self):

        elements = self._elem.findall('.//a2a:Event', namespaces=self.NS)
        self.events = [models.Event(el)
                       for el in elements]  # or should this be a generator?

        for e in self.events:
            self._refs['event'][e.id] = e

    def _parseObjects(self):

        elements = self._elem.findall('.//a2a:Object', namespaces=self.NS)
        self.objects = [models.Object(el)
                        for el in elements]  # or should this be a generator?

        for o in self.objects:
            self._refs['object'][o.id] = o

    def _parseSource(self):
        self.source = models.Source(
            self._elem.find('.//a2a:Source', namespaces=self.NS))

    def _parseRelations(self):
        """
        Relation factory.
        """

        elements = [i for i in self._elem.iter() if 'Relation' in i.tag]

        relations = []
        for el in elements:
            if 'RelationEP' in el.tag:
                relation = models.RelationEP(el)
            elif 'RelationPP' in el.tag:
                relation = models.RelationPP(el)
            elif 'RelationPO' in el.tag:
                relation = models.RelationPO(el)
            elif 'RelationEO' in el.tag:
                relation = models.RelationEO(el)
            elif 'RelationP' in el.tag:
                relation = models.RelationP(el)
            elif 'RelationOO' in el.tag:
                relation = models.RelationOO(el)
            elif 'RelationO' in el.tag:
                relation = models.RelationO(el)
            else:
                relation = None

            # And make references to instantiated objects
            if hasattr(relation, 'person'):
                person = self._refs['person'][relation.person]
                relation.person = person
                person.relations.append(relation)

            if hasattr(relation, 'event'):
                event = self._refs['event'][relation.event]
                relation.event = event
                event.relations.append(relation)

            if hasattr(relation, 'object'):
                obj = self._refs['object'][relation.object]
                relation.object = obj
                obj.relations.append(relation)

            if hasattr(relation, 'persons'):
                p1 = self._refs['person'][relation.persons[0]]
                p2 = self._refs['person'][relation.persons[1]]
                relation.persons = (p1, p2)
                p1.relations.append(relation)
                p2.relations.append(relation)

            if hasattr(relation, 'objects'):
                o1 = self._refs['object'][relation.objects[0]]
                o2 = self._refs['object'][relation.objects[1]]
                relation.objects = (o1, o2)
                o1.relations.append(relation)
                o2.relations.append(relation)

            relations.append(relation)

        self.relations = relations

    def getEntities(self):

        entities = self.persons + self.events + self.objects + \
            self.relations + [self.source]

        return [i for i in entities if i]

    def toRDF(self):
        pass


if __name__ == "__main__":

    dc = DocumentCollection(
        '/home/leon/Documents/Golden_Agents/saaA2A/data/a2a/SAA-ID-001_SAA_Index_op_notarieel_archief/000000001.xml'
        # '/home/leon/Documents/Golden_Agents/saaA2A/data/a2a/SAA-ID-002_SAA_Index_op_doopregisters/000000001.xml'
    )

    # d = Document(
    #     '/home/leon/Documents/Golden_Agents/A2A/pya2a/pya2a/test/saa_list.xml')

    for d in dc:
        for p in d.persons:
            print(p.Remarks)

    # documents = []
    # folder = '/media/leon/My Book/index/4018f750-f13f-6123-229f-0e86942219bb'

    # for n, f in enumerate(os.listdir(folder), 1):

    #     filepath = os.path.join(folder, f)

    #     documentCollection = DocumentCollection(filepath)

    #     for d in documentCollection.documents:
    #         print(vars(d))
