#!/usr/bin/env python
import json
from subprocess import Popen, PIPE
import sys
import textwrap



# Typical command line usage:
#
# python graphdeps.py TASKFILTER
#
# TASKFILTER is a taskwarrior filter, documentation can be found here: http://taskwarrior.org/projects/taskwarrior/wiki/Feature_filters
#
# Probably the most helpful commands are:
#
# python graphdeps.py project:fooproject status:pending  
#  --> graph pending tasks in project 'fooproject'
#
# python graphdeps.py project:fooproject
#  --> graphs all tasks in 'fooproject', pending, completed, deleted
#
# python graphdeps.py status:pending
#  --> graphs all pending tasks in all projects
#
# python graphdeps.py
#  --> graphs everything - could be massive
#


#Wrap label text at this number of characters
charsPerLine = 20;

#full list of colors here: http://www.graphviz.org/doc/info/colors.html
blockedColor = 'gold4'
maxUrgencyColor = 'red2'
unblockedColor = 'green'
doneColor = 'grey'
waitColor = 'white'
deletedColor = 'pink'
tagColor = 'white'

#The width of the border around the tasks:
penWidth = 1

#Left to right layout, my favorite, ganntt-ish
HEADER = "digraph  dependencies { splines=true; overlap=ortho; rankdir=LR; weight=2;"

#Spread tasks on page
#HEADER = "digraph  dependencies { layout=neato;   splines=true; overlap=scalexy;  rankdir=LR; weight=2;"

#More information on setting up graphviz: http://www.graphviz.org/doc/info/attrs.html

FOOTER = "}"

JSON_START = '['
JSON_END = ']'

validUuids = list()

def call_taskwarrior(cmd):
    'call taskwarrior, returning output and error'
    tw = Popen(['task'] + cmd.split(), stdout=PIPE, stderr=PIPE)
    return tw.communicate()

def get_json(query):
    'call taskwarrior, returning objects from json'
    result, err = call_taskwarrior('export %s' % query)
    return json.loads(JSON_START + result + JSON_END)

def call_dot(instruction):
    'call dot, returning stdout and stdout'
    print(instruction)
    dot = Popen('circo -T png'.split(), stdout=PIPE, stderr=PIPE, stdin=PIPE)
    return dot.communicate(instruction)


query = sys.argv[1:]
data = get_json(' '.join(query))
#print data

# fill in possible tags, they are going to be the center
# of the network
allTags = set()
for datum in data:
    if 'tags' in datum.keys():
        for tag in datum['tags']:
            if tag not in allTags:
                allTags.add(tag)
tags = {}
for (tag, i) in zip(allTags, range(len(allTags))):
    tags[tag] = i

maxUrgency = -9999;
for datum in data:
    if float(datum['urgency']) > maxUrgency:
        maxUrgency = float(datum['urgency'])


### first pass: task nodes
lines = [HEADER]
for datum in data:
    validUuids.append(datum['uuid'])
    if datum['description']:

        style = ''
        color = ''
        style = 'filled'

        if datum['status']=='pending':
            prefix = datum['id']
            if not datum.get('depends','') : color = unblockedColor
            else :
                hasPendingDeps = 0
                for depend in datum['depends'].split(','):
                    for datum2 in data:
                        if datum2['uuid'] == depend and datum2['status'] == 'pending':
                            hasPendingDeps = 1
                if hasPendingDeps == 1 : color = blockedColor
                else : color = unblockedColor

        elif datum['status'] == 'waiting':
            prefix = 'WAIT'
            color = waitColor
        elif datum['status'] == 'completed':
            prefix = 'DONE'
            color = doneColor
        elif datum['status'] == 'deleted':
            prefix = 'DELETED'
            color = deletedColor
        else:
            prefix = ''
            color = 'white'


        if float(datum['urgency']) == maxUrgency:
            color = maxUrgencyColor

        label = '';
        descriptionLines = textwrap.wrap(datum['description'],charsPerLine);
        for descLine in descriptionLines:
            label += descLine+"\\n";

        lines.append('"%s"[shape=note][penwidth=%d][label="%s\:%s"][fillcolor=%s][style=%s]' % (datum['uuid'], penWidth, prefix, label, color, style))


### second pass: write down tags
for tag in tags:
    line = "\"tag{0}\"".format(tags[tag])
    line += "[shape=ellipse]"
    line += "[label=\"{0}\"]".format(tag)
    line += "[fillcolor=black]"
    line += "[style=filled]"
    line += "[fontcolor=white]"
    lines.append(line)


### third pass: task dependencies
for datum in data:
    if datum['description']:
        for dep in datum.get('depends', '').split(','):
            #print ("\naaa %s" %dep)
            if dep!='' and dep in validUuids:
                lines.append('"%s" -> "%s"[style=bold];' % (dep, datum['uuid']))
                continue


### fourth pass: tag dependencies
for datum in data:
    if 'tags' in datum.keys():
        for tag in datum['tags']:
            if tag in tags.keys():
                line = "\"tag{0}\" -> \"{1}\"[style=dashed];".format(tags[tag], datum['uuid'])
                lines.append(line)


lines.append(FOOTER)

png, err = call_dot('\n'.join(lines))
if err != '':
    print ('Error calling dot:')
    print (err.strip())

print ('Writing to deps.png')
with open('deps.png', 'w') as f:
    f.write(png)


