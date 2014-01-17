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
    print(list(filter(lambda x: x != [], res)))
    return res

def tagVSproject(self):
        pass


class Dotter(object):

    def __init__(self, conf, connects):
        self.HEADER = "digraph  dependencies {"
        self.HEADER += "layout={0}; ".format(conf.layout)
        self.HEADER += "splines=true; "
        self.HEADER += "overlap=scalexy; "
        self.HEADER += "rankdir=LR;"
        self.HEADER += "weight=2;"
        self.FOOTER = "}"
        self.connects = connects
        self.layout = conf.layout
        self.misc = conf.misc
        self.colors = conf.colors
        self.weights = conf.weights


    def project(self, project):
        line = "\"{0}\"".format(project)
        line += "[shape=diamond]"
        line += "[label=\"{0}\"]".format(project)
        line += "[color=blue]"
        line += "[style=bold]"
        line += "[fontcolor=red]"
        line += "[fontsize=12]"
        return line


    def tag(self, tag):
        line = "\"{0}\"".format(tag)
        line += "[shape=ellipse]"
        line += "[label=\"{0}\"]".format(tag)
        line += "[fillcolor=black]"
        line += "[style=filled]"
        line += "[fontcolor=white]"
        return line


    def annotation(self, anno):
        label = ''
        descriptionLines = textwrap.wrap(anno.description,
                                         self.misc.charsPerLine)
        for descLine in descriptionLines:
            label += descLine + "\\n";
        res = '"{0}"'.format(anno.entry)
        res += '[shape=note]'
        res += '[penwidth={0}]'.format(self.misc.penWidth)
        res += '[label="{0}"]'.format(label)
        res += '[fillcolor={0}]'.format(self.colors.annotation)
        res += '[style=filled]'
        return res

    def tags(self, tags):
        return list(map(self.tag, tags))

    def projects(self, projects):
        return list(map(self.project, projects))

    def annotations(self, annotations):
        h = [self.annotation(a) for a in annotations]
        return h

    def task(self, tasks, task, excludedTaskStatus, excludedAnnotationStatus):

        style = ''
        color = ''
        style = 'filled'

        if task['status'] in excludedTaskStatus:
            return ''

        if task['status'] == 'pending':
            prefix = ''
            if not 'depends' in task:
                color = self.colors.unblocked
            else :
                hasPendingDeps = False
                for depend in task['depends'].split(','):
                    for t in tasks:
                        if t['uuid'] == depend and not t['status'] in excludedAnnotationStatus:
                            hasPendingDeps = True
                if hasPendingDeps:
                    color = self.colors.blocked
                else:
                    color = self.colors.unblocked

        elif task['status'] == 'waiting':
            prefix = 'WAIT'
            color = self.colors.wait
        elif task['status'] == 'completed':
            prefix = 'DONE'
            color = self.colors.done
        elif task['status'] == 'deleted':
            prefix = 'DELETED'
            color = self.colors.deleted
        else:
            prefix = ''
            color = self.colors.other

        label = '';
        descriptionLines = textwrap.wrap(task['description'],
                                         self.misc.charsPerLine);
        for descLine in descriptionLines:
            label += descLine + "\\n";

        line = '"{0}"'.format(task['uuid'])
        line += '[shape=box]'
        line += '[penwidth={0}]'.format(self.misc.penWidth)
        line += '[label="{0}: {1}"]'.format(prefix, label)
        line += '[fillcolor={0}]'.format(color)
        line += '[style={0}]'.format(style)

        return line


    def nodesVSnodes(self, con):
        line = '"{0}" -> "{1}"'.format(con.id1, con.id2)
        line += '[style={0}]'.format(con.style)
        line += '[color={0}]'.format(con.color)
        line += '[weight={0}]'.format(con.weight)
        return line



    def inputString(self, tasks, collection, conf):
        res = [self.HEADER]

        # nodes
        for task in tasks:
            res.append(self.task(tasks,
                                 task,
                                 conf.excluded.taskStatus,
                                 conf.excluded.annotationStatus))
        if conf.nodes.projects:
            res = res + self.projects(collection.projects)
        if conf.nodes.tags:
            res = res + self.tags(collection.tags)
        if conf.nodes.annotations:
            res = res + self.annotations(collection.annotations)

        # edges
        for con in self.connects:
            res.append(self.nodesVSnodes(con))

        res.append(self.FOOTER)

        return "\n".join(res)


