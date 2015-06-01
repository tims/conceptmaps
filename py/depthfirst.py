from collections import defaultdict


class Concept:
    def __init__(self, extent, intent):
        self.extent = set(extent)
        self.intent = set(intent)


class Context:
    def __init__(self, pairs):
        self.objectToAttributes = defaultdict(list)
        self.attributeToObjects = defaultdict(list)
        self.objects = set()
        self.attributes = set()
        for pair in pairs:
            obj, attr = pair[0], pair[1]
            self.objects.add(obj)
            self.attributes.add(attr)
            self.objectToAttributes[obj].append(attr)
            self.attributeToObjects[attr].append(obj)

    def sorted_attributes(self):
        return sorted(list(self.attributes))

    def intent(self, objects):
        if not objects:
            return self.attributes
        else:
            # attribute_lists = (self.objectToAttributes[obj] for obj in objects)
            intent = []
            for y in self.attributes:
                yes = True
                for x in objects:
                    if y not in self.objectToAttributes[x]:
                        yes = False
                if yes:
                    intent.append(y)
            return set(intent)
            #return reduce(lambda accum, attrs: accum.intersection(attrs), attribute_lists, set())

    def extent(self, attributes):
        if not attributes:
            return self.objects
        else:
            extent = []
            for x in self.objects:
                yes = True
                for y in attributes:
                    if x not in self.attributeToObjects[y]:
                        yes = False
                if yes:
                    extent.append(x)
            return set(extent)
            # object_lists = (self.attributeToObjects[obj] for obj in attributes)
            # return reduce(lambda accum, attrs: accum.union(attrs), object_lists, set())


def generate_from(context, concept, attribute_y):
    print 'generate_from', attribute_y
    context_attributes = context.sorted_attributes()
    y = context_attributes.index(attribute_y)
    concepts = []
    for attribute_j in context_attributes[y:]:
        print 'attribute_j', attribute_j
        if attribute_j in concept.intent:
            pass
        else:
            j = context_attributes.index(attribute_j)
            extent_j = context.extent([attribute_j])
            extent = set(concept.extent).intersection(extent_j)
            intent = context.intent(extent)
            concept_j = Concept(extent, intent)

            extent_ = context.extent(list(concept.intent) + [attribute_j])
            intent_ = context.intent(extent_)

            processed_attributes = filter(lambda attr: attr < attribute_j, context.attributes)

            print 'j', attribute_j
            print 'extent', context.extent(intent), extent
            print 'intent', context.intent(extent), intent
            print 'extent_, intent_', list(concept.intent) + [attribute_j], extent_, intent_

            print len(extent.difference(context.extent(intent))) != 0
            print len(extent) != len(context.extent(intent))
            if len(extent) != len(context.extent(intent)):
                raise 'bla'
            if len(intent) != len(context.intent(extent)):
                print ('not a concept')
                print intent == context.intent(concept.extent)
                print len(intent.intersection(context.intent(concept.extent))) == 0
                print intent, context.intent(concept.extent)
                print 'intent', context.intent(extent), intent
                print 'extent', context.extent(intent), extent
                print 'intent.difference(context.intent(concept.extent))', intent.difference(
                    context.intent(concept.extent))
                raise 'bla2'

            concepts.append(concept_j)

            if concept.intent.intersection(processed_attributes) != concept_j.intent.intersection(processed_attributes):
                if j < len(context.attributes) - 1:
                    concepts + generate_from(context, concept_j, context_attributes[attribute_j])
    return concepts


if __name__ == '__main__':
    context = Context([
        ('a', 1),
        ('b', 2),
        ('b', 3),
        ('c', 3),
        ('d', 3),
        ('e', 2),
        ('f', 2),
        ('g', 1),
        ('g', 4),
        ('g', 2)
    ])

    initial_concept = Concept(context.extent([]), context.intent(context.extent([])))

    concepts = generate_from(context, initial_concept, 1)
    for concept in concepts:
        print 'concept', concept.intent, concept.extent
