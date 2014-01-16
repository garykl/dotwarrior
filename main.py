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
HEADER = "digraph  dependencies { layout=circo;   splines=true; overlap=scalexy;  rankdir=LR; weight=2;"
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
    dot = Popen('dot -T png'.split(), stdout=PIPE, stderr=PIPE, stdin=PIPE)
    return dot.communicate(instruction)


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



def tag2dot(tag):
    line = "\"{0}\"".format(tag)
    line += "[shape=ellipse]"
    line += "[label=\"{0}\"]".format(tag)
    line += "[fillcolor=black]"
    line += "[style=filled]"
    line += "[fontcolor=white]"
    return line


def tags2dot(tags):
    lines = []
    for tag in tags:
        lines.append(tag2dot(tag))
    return lines


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
                if tag in tags:
                    line = "\"{0}\" -> \"{1}\"[style=dashed];".format(tag, task['uuid'])
                    res.append(line)
    return res


query = sys.argv[1:]
data = get_json(' '.join(query))

# data has to be queried somehow

tags = tagsFromData(data)
uuids = uuidsFromData(data)

lines = [HEADER]

# nodes
for datum in data:
    lines.append(prepareTask(datum))
lines = lines + tags2dot(tags)

# edges
for datum in data:
    lines = lines + taskVStask2dot(datum)

for datum in data:
    lines = lines + taskVStag2dot(datum)

lines.append(FOOTER)

png, err = call_dot('\n'.join(lines))
if err != '':
    print ('Error calling dot:')
    print (err.strip())

print ('Writing to deps.png')
with open('deps.png', 'w') as f:
    f.write(png)


