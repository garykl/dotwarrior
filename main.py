#!/usr/bin/env python
import json
from subprocess import Popen, PIPE
import sys
import textwrap

# Typical command line usage:
#
# python graphdeps.py TASKFILTER
#
# TASKFILTER is a taskwarrior filter, documentation can be found here:
# http://taskwarrior.org/projects/taskwarrior/wiki/Feature_filters
# setting up graphviz:
# http://www.graphviz.org/doc/info/attrs.html
# available colors
# full list of colors here: http://www.graphviz.org/doc/info/colors.html


### basic configuration:

## what is a node?
tagsASnodes = True
projectsASnodes = True

## fine tune node existence and connection creation
excludedTags = ['program'] # those nodes are supressed
excludedTaggedTaskStatus = set(['completed', 'deleted']) # connection between tags and those are supressed
excludedTaskStatus = ['deleted'] # nodes removed
for e in excludedTaskStatus:  # excluded tasks do not need connections
    excludedTaggedTaskStatus.add(e)

## edges weight
class Weight(object):
    def __init__(self):
        self.task2task = 3
        self.task2tag  = 1
        self.task2project = 6
weight = Weight()

## layout
layout = "fdp"
class Misc(object):
    def __init__(self):
        self.charsPerLine = 20;
        self.penWidth = 1
misc = Misc()

# colors
class Colors(object):
    def __init__(self):
        self.blockedColor = 'gold4'
        self.unblockedColor = 'green'
        self.doneColor = 'grey'
        self.waitColor = 'white'
        self.deletedColor = 'pink'
        self.tagColor = 'white'
        self.elseColor = 'white'
colors = Colors()

## graphviz
# Left to right layout, my favorite, ganntt-ish
# HEADER = "digraph  dependencies { splines=true; overlap=ortho; rankdir=LR; weight=2;"
# Spread tasks on page
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


    def taskVStask(self, task):
        res = []
        if task['description']:
            for dep in task.get('depends', '').split(','):
                if dep != '' and dep in uuids:
                    res.append('"%s" -> "%s"[style=bold];' % (dep, task['uuid']))
        return res


    def taskVStag(self, task):
        res = []
        if task['description']:
            if 'tags' in task.keys():
                for tag in task['tags']:
                    if tag in tags and not task['status'] in excludedTaggedTaskStatus:
                        line = "\"{0}\" -> \"{1}\"[style=dashed];".format(tag, task['uuid'])
                        res.append(line)
        return res


    def taskVSproject(self,task):
        res = []
        if task['description']:
            if 'project' in task.keys():
                if not task['status'] in excludedTaskStatus:
                    project = task['project']
                    line = "\"{0}\" -> \"{1}\"[style=bold][color=blue];".format(project, task['uuid'])
                    res.append(line)
        return res


    def task(self,task):

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
                    for task in data:
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
        line += '[shape=note]'
        line += '[penwidth={0}]'.format(self.misc.penWidth)
        line += '[label="{0}: {1}"]'.format(prefix, label)
        line += '[fillcolor={0}]'.format(color)
        line += '[style={0}]'.format(style)

        return line


    def inputString(self):
        res = [self.HEADER]

        # nodes
        for datum in data:
            res.append(self.task(datum))
        if projectsASnodes:
            res = res + self.projects(projects)
        if tagsASnodes:
            res = res + self.tags(tags)

        # edges
        for datum in data:
            res = res + self.taskVStask(datum)
        if tagsASnodes:
            for datum in data:
                res = res + self.taskVStag(datum)
        if projectsASnodes:
            for datum in data:
                res = res + self.taskVSproject(datum)

        res.append(self.FOOTER)

        return "\n".join(res)



def call_taskwarrior(cmd):
    'call taskwarrior, returning output and error'
    tw = Popen(['task'] + cmd.split(), stdout=PIPE, stderr=PIPE)
    return tw.communicate()


def get_json(query):
    'call taskwarrior, returning objects from json'
    JSON_START = '['
    JSON_END = ']'
    result, err = call_taskwarrior('export %s' % query)
    return json.loads(JSON_START + result.decode('utf8') + JSON_END)


def call_dot(instruction):
    'call dot, returning stdout and stdout'
    dot = Popen('dot -T svg'.split(), stdout=PIPE, stderr=PIPE, stdin=PIPE)
    return dot.communicate(instruction.encode())


def projectsFromTasks(tasks):
    res = set()
    for task in tasks:
        if 'project' in task.keys():
            res.add(task['project'])
    return res


def tagsFromData(data):
    """
    data is list of dictionaries, containing data from
    the export function of taskwarrior.
    return a set with the keys.
    """
    allTags = set()
    for datum in data:
        if 'tags' in datum.keys():
            for tag in datum['tags']:
                if tag not in allTags:
                    allTags.add(tag)
    return allTags


def uuidsFromData(data):
    res = []
    for datum in data:
        res.append(datum['uuid'])
    return res


def excludeElementsFrom(toExclude, ll):
    """
    toExclude and ll are lists of elements.
    return a new list, containing all elements of ll,
    which are not in toExclude.
    """
    res = []
    for l in ll:
        if not l in toExclude:
            res.append(l)
    return res



query = sys.argv[1:]
data = get_json(' '.join(query))

# data has to be queried somehow
projects = projectsFromTasks(data)
tags = excludeElementsFrom(excludedTags, tagsFromData(data))
uuids = uuidsFromData(data)

# dotfile
dotter = Dotter(layout, colors, weight, misc)
dotSource = dotter.inputString()
#:print(dotSource)

## calling dot
png, err = call_dot(dotSource)
if err != b'':
    print ('Error calling dot:')
    print (err.strip())

print ('Writing to deps.svg')
with open('deps.svg', 'w') as f:
    f.write(png.decode('utf-8'))


