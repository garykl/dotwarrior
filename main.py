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
excludedTaggedTaskStatus = ['completed', 'deleted'] # connection between tags and those are supressed

# Wrap label text at this number of characters
charsPerLine = 20;
# The width of the border around the tasks:
penWidth = 1

# colors
blockedColor = 'gold4'
unblockedColor = 'green'
doneColor = 'grey'
waitColor = 'white'
deletedColor = 'pink'
tagColor = 'white'

## graphviz
# Left to right layout, my favorite, ganntt-ish
# HEADER = "digraph  dependencies { splines=true; overlap=ortho; rankdir=LR; weight=2;"
# Spread tasks on page
HEADER = "digraph  dependencies { layout=sfdp;   splines=true; overlap=scalexy;  rankdir=LR; weight=2;"
FOOTER = "}"

def call_taskwarrior(cmd):
    'call taskwarrior, returning output and error'
    tw = Popen(['task'] + cmd.split(), stdout=PIPE, stderr=PIPE)
    return tw.communicate()


def get_json(query):
    'call taskwarrior, returning objects from json'
    JSON_START = '['
    JSON_END = ']'
    result, err = call_taskwarrior('export %s' % query)
    return json.loads(JSON_START + result + JSON_END)


def call_dot(instruction):
    'call dot, returning stdout and stdout'
    dot = Popen('dot -T svg'.split(), stdout=PIPE, stderr=PIPE, stdin=PIPE)
    return dot.communicate(instruction)


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


def prepareTask(task):

    style = ''
    color = ''
    style = 'filled'

    if task['status']=='pending':
        prefix = ''
        if not task.get('depends',''):
            color = unblockedColor
        else :
            hasPendingDeps = 0
            for depend in task['depends'].split(','):
                for task in data:
                    if task['uuid'] == depend and task['status'] == 'pending':
                        hasPendingDeps = 1
            if hasPendingDeps == 1 : color = blockedColor
            else : color = unblockedColor

    elif task['status'] == 'waiting':
        prefix = 'WAIT'
        color = waitColor
    elif task['status'] == 'completed':
        prefix = 'DONE'
        color = doneColor
    elif task['status'] == 'deleted':
        prefix = 'DELETED'
        color = deletedColor
    else:
        prefix = ''
        color = 'white'

    label = '';
    descriptionLines = textwrap.wrap(task['description'],charsPerLine);
    for descLine in descriptionLines:
        label += descLine+"\\n";

    line = '"{0}"'.format(task['uuid'])
    line += '[shape=note]'
    line += '[penwidth={0}]'.format(penWidth)
    line += '[label="{0}: {1}"]'.format(prefix, label)
    line += '[fillcolor={0}]'.format(color)
    line += '[style={0}]'.format(style)

    return line


def project2dot(project):
    line = "\"{0}\"".format(project)
    line += "[shape=diamond]"
    line += "[label=\"{0}\"]".format(project)
    line += "[color=blue]"
    line += "[style=bold]"
    line += "[fontcolor=blue]"
    line += "[fontsize=10]"
    return line


def tag2dot(tag):
    line = "\"{0}\"".format(tag)
    line += "[shape=ellipse]"
    line += "[label=\"{0}\"]".format(tag)
    line += "[fillcolor=black]"
    line += "[style=filled]"
    line += "[fontcolor=white]"
    return line


def list2dot(ll, f):
    " convert a list to dot-file lines using the function f "
    lines = []
    for l in ll:
        lines.append(f(l))
    return lines


def tags2dot(tags):
    return list2dot(tags, tag2dot)


def projects2dot(projects):
    return list2dot(projects, project2dot)


def taskVStask2dot(task):
    res = []
    if task['description']:
        for dep in task.get('depends', '').split(','):
            if dep != '' and dep in uuids:
                res.append('"%s" -> "%s"[style=bold];' % (dep, task['uuid']))
    return res


def taskVStag2dot(task):
    res = []
    if task['description']:
        if 'tags' in task.keys():
            for tag in task['tags']:
                if tag in tags and task['status'] not in excludedTaggedTaskStatus:
                    line = "\"{0}\" -> \"{1}\"[style=dashed];".format(tag, task['uuid'])
                    res.append(line)
    return res


def taskVSproject2dot(task):
    res = []
    if task['description']:
        if 'project' in task.keys():
            project = task['project']
            line = "\"{0}\" -> \"{1}\"[style=bold][color=blue];".format(project, task['uuid'])
            res.append(line)
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
print(call_taskwarrior(' '.join(query))[0])

# data has to be queried somehow

projects = projectsFromTasks(data)
tags = excludeElementsFrom(excludedTags, tagsFromData(data))
uuids = uuidsFromData(data)

lines = [HEADER]

# nodes
for datum in data:
    lines.append(prepareTask(datum))
if projectsASnodes:
    lines = lines + projects2dot(projects)
if tagsASnodes:
    lines = lines + tags2dot(tags)

# edges
for datum in data:
    lines = lines + taskVStask2dot(datum)

if tagsASnodes:
    for datum in data:
        lines = lines + taskVStag2dot(datum)

if projectsASnodes:
    for datum in data:
        lines = lines + taskVSproject2dot(datum)


lines.append(FOOTER)

png, err = call_dot('\n'.join(lines))
if err != '':
    print ('Error calling dot:')
    print (err.strip())

print ('Writing to deps.svg')
with open('deps.svg', 'w') as f:
    f.write(png)


