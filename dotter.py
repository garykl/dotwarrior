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


    def list(self, ll, f):
        " convert a list to dot-file lines using the function f "
        lines = []
        for l in ll:
            lines.append(f(l))
        return lines


    def tags(self, tags):
        return self.list(tags, self.tag)


    def projects(self, projects):
        return self.list(projects, self.project)


    def taskVStask(self, task, uuids):
        res = []
        if task['description']:
            for dep in task.get('depends', '').split(','):
                if dep != '' and dep in uuids:
                    res.append('"%s" -> "%s"[style=bold];' % (dep, task['uuid']))
        return res


    def taskVStag(self, task, tags, excludedTaggedTaskStatus):
        res = []
        if task['description']:
            if 'tags' in task.keys():
                for tag in task['tags']:
                    if tag in tags and not task['status'] in excludedTaggedTaskStatus:
                        line = "\"{0}\" -> \"{1}\"[style=dashed];".format(tag, task['uuid'])
                        res.append(line)
        return res


    def taskVSproject(self,task, excludedTaskStatus):
        res = []
        if task['description']:
            if 'project' in task.keys():
                if not task['status'] in excludedTaskStatus:
                    project = task['project']
                    line = "\"{0}\" -> \"{1}\"[style=bold][color=blue];".format(project, task['uuid'])
                    res.append(line)
        return res


    def task(self, tasks, task, excludedTaskStatus):

        style = ''
        color = ''
        style = 'filled'

        if task['status'] in excludedTaskStatus:
            return ''

        if task['status'] == 'pending':
            prefix = ''
            if not task.get('depends',''):
                color = self.colors.unblockedColor
            else :
                hasPendingDeps = 0
                for depend in task['depends'].split(','):
                    for task in tasks:
                        if task['uuid'] == depend and task['status'] == 'pending':
                            hasPendingDeps = 1
                if hasPendingDeps == 1 : color = self.colors.blockedColor
                else : color = self.colors.unblockedColor

        elif task['status'] == 'waiting':
            prefix = 'WAIT'
            color = self.colors.waitColor
        elif task['status'] == 'completed':
            prefix = 'DONE'
            color = self.colors.doneColor
        elif task['status'] == 'deleted':
            prefix = 'DELETED'
            color = self.colors.deletedColor
        else:
            prefix = ''
            color = self.colors.elseColor;

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
                    tagsASnodes, projectsASnodes):
        res = [self.HEADER]

        # nodes
        for task in tasks:
            res.append(self.task(tasks, task, excludedTaskStatus))
        if projectsASnodes:
            res = res + self.projects(collection.projects)
        if tagsASnodes:
            res = res + self.tags(collection.tags)

        # edges
        for task in tasks:
            res = res + self.taskVStask(task, collection.uuids)
        if tagsASnodes:
            for task in tasks:
                res = res + self.taskVStag(task, collection.tags, excludedTaggedTaskStatus)
        if projectsASnodes:
            for task in tasks:
                res = res + self.taskVSproject(task, excludedTaskStatus)

        res.append(self.FOOTER)

        return "\n".join(res)


