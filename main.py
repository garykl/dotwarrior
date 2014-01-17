#!/usr/bin/env python
import sys

from extern import dot, taskwarriorJSON
from dotter import Dotter, connector
from collector import Collector
from config import Conf
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


query = sys.argv[1:]
conf = Conf()

tasks = taskwarriorJSON(' '.join(query))

# data has to be queried somehow

# dotfile
collections = Collector(tasks, conf.excluded.tags)
connects = connector(conf, collections, tasks)
dotter = Dotter(conf, connects)
dotSource = dotter.inputString(tasks, collections, conf)

#:print(dotSource)
## calling dot
png, err = dot(dotSource)
if err != b'':
    print ('Error calling dot:')
    print (err.strip())

print ('Writing to deps.svg')
with open('deps.svg', 'w') as f:
    f.write(png.decode('utf-8'))


