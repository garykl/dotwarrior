#!/usr/bin/env python3
import sys

from extern import interpreteInput, dot, taskwarriorJSON
from dotter import dotCode, connector, nodes
from collector import Collector
from config import configs
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

(confKeys, taskWarriorArgs) = interpreteInput(sys.argv[1:])

## read data
tasks = taskwarriorJSON(taskWarriorArgs)

for conf in [configs[c] for c in confKeys]:

    ## prepare data
    collections = Collector(tasks, conf.excluded.tags)

    connects = connector(conf, collections, tasks)
    nods = nodes(conf, collections, tasks)

    ## write data
    dotSource = dotCode(conf, nods, connects)

    ## calling dot
    dot(conf, dotSource)

