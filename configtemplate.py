class Miscs(object):
    def __init__(self):
        self.charsPerLine = 20;
        self.penwidth = 1

# colors
class Colors(object):
    def __init__(self):
        self.project = 'white'
        self.annotation = 'yellow'
        self.blocked = 'green'
        self.unblocked = 'lightgreen'
        self.done = 'grey'
        self.wait = 'white'
        self.deleted = 'pink'
        self.tag = 'white'
        self.other = 'white'

## what is a node?
class Nodes(object):
    def __init__(self):
        self.tasks = True
        self.tags = True
        self.projects = True
        self.annotations = True

## fine tune node existence and connection creation
class Excluded(object):
    def __init__(self):
        self.tags = [] # those nodes are supressed
        self.taskStatus = ['deleted'] # nodes removed
        self.taggedTaskStatus = set(['deleted']) # connection between tags and those are supressed
        self.annotationStatus = ['deleted', 'completed']
        # excluded tasks do not need connections

## edges weight
class Weights(object):
    def __init__(self):
        self.task2task = 11
        self.task2tag  = 1
        self.task2project = 6
        self.task2annotation = 99


class Conf(object):
    def __init__(self):
        self.filename = 'dotwarrior.svg'
        self.layout = "neato"
        self.colors = Colors()
        self.weights = Weights()
        self.misc = Miscs()
        self.excluded = Excluded()
        self.nodes = Nodes()

