#!/usr/bin/env python
import sys

from extern import dot, taskwarriorJSON
from dotter import Dotter
from collector import Collector
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








query = sys.argv[1:]
data = taskwarriorJSON(' '.join(query))

# data has to be queried somehow

# dotfile
dotter = Dotter(layout, colors, weight, misc)
collection = Collector(data, excludedTags)
dotSource = dotter.inputString(data, collection,
                               excludedTaskStatus, excludedTaggedTaskStatus,
                               tagsASnodes, projectsASnodes)
#:print(dotSource)

## calling dot
png, err = dot(dotSource)
if err != b'':
    print ('Error calling dot:')
    print (err.strip())

print ('Writing to deps.svg')
with open('deps.svg', 'w') as f:
    f.write(png.decode('utf-8'))


