import textwrap


class Dotter(object):

    def __init__(self,
                 layout,
                 colors,
                 weight,
                 misc):
        self.HEADER = "digraph  dependencies {"
        self.HEADER += "layout={0}; ".format(layout)
        self.HEADER += "splines=true; "
        self.HEADER += "overlap=scalexy; "
        self.HEADER += "rankdir=LR;"
        self.HEADER += "weight=2;"
        self.FOOTER = "}"
        self.layout = layout
        self.misc = misc
        self.colors = colors
        self.weight = weight


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

    def taskVStask(self, task, uuids):
        res = []
        if task['description']:
            for dep in task.get('depends', '').split(','):
                if dep != '' and dep in uuids:
                    line = '"{0}" -> "{0}"'.format(dep, task['uuid'])
                    line += '[style=bold]'
                    line += '[weight={0}]'.format(self.weight.task2task)
                    res.append(line)
        return res


    def taskVStag(self, task, tags, excludedTaggedTaskStatus):
        res = []
        if task['description']:
            if 'tags' in task.keys():
                for tag in task['tags']:
                    if tag in tags and not task['status'] in excludedTaggedTaskStatus:
                        line = "\"{0}\" -> \"{1}\"".format(tag, task['uuid'])
                        line += '[style=dashed]'
                        line += '[weight={0}];'.format(self.weight.task2tag)
                        res.append(line)
        return res


    def taskVSproject(self,task, excludedTaskStatus):
        res = []
        if task['description']:
            if 'project' in task.keys():
                if not task['status'] in excludedTaskStatus:
                    project = task['project']
                    line = "\"{0}\" -> \"{1}\"".format(project, task['uuid'])
                    line += '[weight={0}]'.format(self.weight.task2project)
                    line += '[style=bold][color=blue]';
                    res.append(line)
        return res


    def taskVSannotation(self, task):
        lines = []
        if 'annotations' in task:
            for a in task['annotations']:
                line = '"{0}" -> "{1}"'.format(a['entry'], task['uuid'])
                line += '[style=solid]'
                line += '[color=green]'
                line += '[weight={0}]'.format(self.weight.task2annotation)
                lines.append(line)
        return lines


    def tagVSproject(self):
        pass


    def task(self, tasks, task, excludedTaskStatus):

        style = ''
        color = ''
        style = 'filled'

        if task['status'] in excludedTaskStatus:
            return ''

        if task['status'] == 'pending':
            prefix = ''
            if not task.get('depends',''):
                color = self.colors.unblocked
            else :
                hasPendingDeps = 0
                for depend in task['depends'].split(','):
                    for task in tasks:
                        if task['uuid'] == depend and task['status'] == 'pending':
                            hasPendingDeps = 1
                if hasPendingDeps == 1 : color = self.colors.blocked
                else : color = self.colors.unblocked

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




    def inputString(self, tasks, collection,
                    excludedTaskStatus, excludedTaggedTaskStatus,
                    tagsASnodes, projectsASnodes, annotationsASnodes):
        res = [self.HEADER]

        # nodes
        for task in tasks:
            res.append(self.task(tasks, task, excludedTaskStatus))
        if projectsASnodes:
            res = res + self.projects(collection.projects)
        if tagsASnodes:
            res = res + self.tags(collection.tags)
        if annotationsASnodes:
            res = res + self.annotations(collection.annotations)

        # edges
        for task in tasks:
            res = res + self.taskVStask(task, collection.uuids)
        if tagsASnodes:
            for task in tasks:
                res = res + self.taskVStag(task, collection.tags, excludedTaggedTaskStatus)
        if projectsASnodes:
            for task in tasks:
                res = res + self.taskVSproject(task, excludedTaskStatus)
        if annotationsASnodes:
            for task in tasks:
                res = res + self.taskVSannotation(task)

        res.append(self.FOOTER)

        return "\n".join(res)


