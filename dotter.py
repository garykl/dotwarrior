# Copright 2014 Gary Klindt
#
# This file is part of dotwarrior.
#
# dotwarrior is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# dotwarrio is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with dotwarrior.  If not, see <http://www.gnu.org/licenses/>.

import textwrap
from extern import taskwarriorUrgency


class Range(object):
    def __init__(self, minimum, maximum):
        self.min = minimum
        self.max = maximum
    def normalize(self, value):
        """
        normalize value, in such a way, that only
        values between 0 and 1 are returned.
        """
        return 0.7 * (value - self.min) / (self.max - self.min)


def connector(conf, collections):
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
        res = []
        if 'project' in task:
            if task['project'] in collections.projects:
                if 'tags' in task:
                    for t in task['tags']:
                        if t in collections.tags:
                            res.append(Ret(t,
                                           task['project'],
                                           'solid',
                                           'red',
                                           conf.weights.project2tag))
        return res

    def tagVStags(task):
        res = []
        if 'tags' in task:
            for t1 in task['tags']:
                for t2 in task['tags']:
                    if t1 != t2:
                        res.append(Ret(t1,
                                       t2,
                                       'solid',
                                       'red',
                                       conf.weights.tag2tag))
        return res

    res = []
    for t in collections.tasks:
        if conf.nodes.tasks:
            res = res + taskVStask(t, collections.uuids)
            if conf.nodes.tags:
                res = res + taskVStags(t, collections.tags, conf.excluded.taggedTaskStatus)
            if conf.nodes.projects:
                res = res + taskVSprojects(t, conf.excluded.taskStatus)
            if conf.nodes.annotations:
                res = res + taskVSannotations(t)
        if conf.edges.projectVStags:
            res = res + projectVStags(t)
        if conf.edges.tagVStags:
            res = res + tagVStags(t)
    return res


def nodes(conf, collections):
    """
    return all necessary information for nodes creation
    by the dot program.
    """
    class Ret(object):
        def __init__(self, id, label, **attrs):
            self.id = id
            self.label = label
            self.shape = attrs.get('shape', 'box')
            self.style = attrs.get('style', 'solid')
            self.fillcolor = attrs.get('fillcolor', 'white')
            self.fontcolor = attrs.get('fontcolor',conf.colors.fontDefault)
            self.fontsize = attrs.get('fontsize', '10')
            self.color = attrs.get('color', 'white')
            self.penwidth = attrs.get('penwidth', conf.misc.penwidth)

    def urgencyRange():
        urgs = {}
        mx = -777
        mn = 777
        for task in collections.tasks:
            urgs[task['uuid']] = taskwarriorUrgency(task['uuid'])
        mx = max(urgs.values())
        mn = min(urgs.values())
        return (Range(mn, mx), urgs)

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
                   fillcolor=conf.colors.fillTag,
                   style='filled',
                   fontcolor=conf.colors.fontTag)

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

    def urgencyTask(t, urg, urgRange):
        # r = '{0:1.2f}'.format(urg / maxUrg).split('.')[1]
        # color = '\"#{0}5555\"'.format(r)
        color = "\"{0:1.2f},0.99,0.5\"".format(urgRange.normalize(urg))
        return Ret(t['uuid'],
                   t['description'],
                   fillcolor=color,
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
                    for t2 in collections.tasks:
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

        return Ret(t['uuid'], '{0}: {1}'.format(prefix, label),
                   shape='box',
                   fillcolor=color,
                   style=style)

    res = []
    if conf.nodes.tasks:
        if conf.colors.byUrgency:
            (maxUrgs, urgencies) = urgencyRange()
            for t in collections.tasks:
                res.append(urgencyTask(t, urgencies[t['uuid']], maxUrgs))
        else:
            for t in collections.tasks:
                res.append(task(t))
    if conf.nodes.projects:
        res = res + list(map(project, collections.projects))
    if conf.nodes.tags:
        res = res + list(map(tag, collections.tags))
    if conf.nodes.annotations:
        res = res + list(map(annotation, collections.annotations))

    return filter(lambda x: x != '', res)


def dotsource(conf, nodes, connections):

    HEADER = "digraph  dependencies {"
    HEADER += "layout={0}; ".format(conf.layout)
    HEADER += "splines=true; "
    HEADER += "overlap=scalexy; "
    HEADER += "rankdir=LR;"
    HEADER += "weight=2;"
    FOOTER = "}"

    def node(n):
        label = '';
        descriptionLines = textwrap.wrap(n.label);
        for descLine in descriptionLines:
            label += descLine + "\\n";

        line = '"{0}"'.format(n.id)
        line += '[label="{0}"]'.format(label)
        line += '[shape={0}]'.format(n.shape)
        line += '[fillcolor={0}]'.format(n.fillcolor)
        line += '[fontcolor={0}]'.format(n.fontcolor)
        line += '[style={0}]'.format(n.style)
        line += '[penwidth={0}]'.format(n.penwidth)
        return line


    def nodeVSnode(con):
        line = '"{0}" -> "{1}"'.format(con.id1, con.id2)
        line += '[style={0}]'.format(con.style)
        line += '[color={0}]'.format(con.color)
        line += '[weight={0}]'.format(con.weight)
        return line

    res = [HEADER]

    # nodes
    for n in nodes:
        res.append(node(n))

    # edges
    for con in connections:
        res.append(nodeVSnode(con))

    res.append(FOOTER)
    return "\n".join(res)
