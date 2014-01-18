import textwrap

## helpers

def connector(conf, collections, tasks):
    """
    generate data structure containing all data
    that is necessary for feeding the connections
    into the dot program.
    """
    class Ret(object): # a list of its instaces is returned
        def __init__(self, id1, id2, style, color, weight):
            self.id1 = id1
            self.id2 = id2
            self.style = style
            self.color = color
            self.weight = weight

    def taskVStask(task, uuids):
        res = []
        if task['description']:
            if 'depends' in task:
                for dep in task['depends'].split(','):
                    if dep in uuids:
                        res.append(Ret(dep, task['uuid'], 'bold', 'black', conf.weights.task2task))
        return res

    def taskVStags(task, tags, excludedTaggedTaskStatus):
        res = []
        if task['description']:
            if 'tags' in task.keys():
                for tag in task['tags']:
                    if tag in tags and not task['status'] in excludedTaggedTaskStatus:
                        res.append(Ret(tag, task['uuid'], 'dashed', 'black', conf.weights.task2tag))
        return res

    def taskVSprojects(task, excludedTaskStatus):
        res = []
        if task['description']:
            if 'project' in task.keys():
                if not task['status'] in excludedTaskStatus:
                    res.append(Ret(task['uuid'], task['project'], 'bold', 'blue', conf.weights.task2project))
        return res

    def taskVSannotations(task):
        res = []
        if task['status'] not in conf.excluded.annotationStatus:
            if 'annotations' in task:
                for a in task['annotations']:
                    res.append(Ret(a['entry'],
                                   task['uuid'],
                                   'solid',
                                   'green',
                                   conf.weights.task2annotation))
        return res

    def projectVStags(task):
        pass

    res = []
    for t in tasks:
        if conf.nodes.tasks:
            res = res + taskVStask(t, collections.uuids)
        if conf.nodes.tags:
            res = res + taskVStags(t, collections.tags, conf.excluded.taggedTaskStatus)
        if conf.nodes.projects:
            res = res + taskVSprojects(t, conf.excluded.taskStatus)
        if conf.nodes.annotations:
            res = res + taskVSannotations(t)
    return res

def tagVSproject(self):
        pass

def nodes(conf, collections, tasks):
    """
    return all necessary information for nodes creation
    by the dot program.
    """
    class Ret(object):
        def __init__(self, id, label, **attrs):
            self.id = id
            self.label = label
            self.shape = attrs.get('shape', 'box')
            self.style = attrs.get('style', '')
            self.fillcolor = attrs.get('fillcolor', 'white')
            self.fontcolor = attrs.get('fontcolor', 'black')
            self.fontsize = attrs.get('fontsize', '10')
            self.color = attrs.get('color', 'black')
            self.penwidth = attrs.get('penwidth', conf.misc.penwidth)

    def project(p):
         return Ret(p, p,
                    shape='diamond',
                    color='blue',
                    style='bold',
                    fontcolor='red',
                    fontsize='12')

    def tag(t):
        return Ret(t, t,
                   shape='ellipse',
                   fillcolor=conf.colors.project,
                   style='filled',
                   fontcolor='white')

    def annotation(a):
        label = ''
        descriptionLines = textwrap.wrap(a.description,
                                         conf.misc.charsPerLine)
        for descLine in descriptionLines:
            label += descLine + "\\n";
        return Ret(a.entry, label,
                   shape='note',
                   fillcolor=conf.colors.annotation,
                   style='filled')

    def task(t):
        style = ''
        color = ''
        style = 'filled'

        if t['status'] in conf.excluded.taskStatus:
            return ''

        if t['status'] == 'pending':
            prefix = ''
            if not 'depends' in t:
                color = conf.colors.unblocked
            else :
                hasPendingDeps = False
                for depend in t['depends'].split(','):
                    for t2 in tasks:
                        if t2['uuid'] == depend:
                            if not t2['status'] in conf.excluded.annotationStatus:
                                hasPendingDeps = True
                if hasPendingDeps:
                    color = conf.colors.blocked
                else:
                    color = conf.colors.unblocked

        elif t['status'] == 'waiting':
            prefix = 'WAIT'
            color = conf.colors.wait
        elif t['status'] == 'completed':
            prefix = 'DONE'
            color = conf.colors.done
        elif t['status'] == 'deleted':
            prefix = 'DELETED'
            color = conf.colors.deleted
        else:
            prefix = ''
            color = conf.colors.other

        label = '';
        descriptionLines = textwrap.wrap(t['description'],
                                         conf.misc.charsPerLine);
        for descLine in descriptionLines:
            label += descLine + "\\n";

        return Ret(t['uuid'], '{0}: {1}'.format(prefix, label),
                   shape='box',
                   fillcolor=color,
                   style=style)

    res = []
    for t in tasks:
        res.append(task(t))
    if conf.nodes.projects:
        res = res + list(map(project, collections.projects))
    if conf.nodes.tags:
        res = res + list(map(tag, collections.tags))
    if conf.nodes.annotations:
        res = res + list(map(annotation, collections.annotations))

    return filter(lambda x: x != '', res)


class Dotter(object):

    def __init__(self, conf):
        self.HEADER = "digraph  dependencies {"
        self.HEADER += "layout={0}; ".format(conf.layout)
        self.HEADER += "splines=true; "
        self.HEADER += "overlap=scalexy; "
        self.HEADER += "rankdir=LR;"
        self.HEADER += "weight=2;"
        self.FOOTER = "}"
        self.layout = conf.layout
        self.misc = conf.misc
        self.colors = conf.colors
        self.weights = conf.weights


    def node(self, n):
        line = '"{0}"'.format(n.id)
        line += '[label="{0}"]'.format(n.label)
        line += '[shape={0}]'.format(n.shape)
        line += '[fillcolor={0}]'.format(n.fillcolor)
        line += '[style={0}]'.format(n.style)
        line += '[penwidth={0}]'.format(n.penwidth)
        return line


    def nodeVSnode(self, con):
        line = '"{0}" -> "{1}"'.format(con.id1, con.id2)
        line += '[style={0}]'.format(con.style)
        line += '[color={0}]'.format(con.color)
        line += '[weight={0}]'.format(con.weight)
        return line



    def inputString(self, nodes, connects):
        res = [self.HEADER]

        # nodes
        for n in nodes:
            res.append(self.node(n))

        # edges
        for con in connects:
            res.append(self.nodeVSnode(con))

        res.append(self.FOOTER)

        return "\n".join(res)


def dotCode(conf, nodes, connects):
    dotter = Dotter(conf)
    return dotter.inputString(nodes, connects)
