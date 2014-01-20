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

class Miscs(object):
    def __init__(self):
        self.charsPerLine = 20;
        self.penwidth = 1

# colors
class Colors(object):
    def __init__(self):
        self.project = 'white'
        self.annotation = 'yellow'
        self.blocked = 'green'
        self.unblocked = 'lightgreen'
        self.done = 'grey'
        self.wait = 'white'
        self.deleted = 'pink'
        self.tag = 'white'
        self.fillTag = 'black'
        self.fontTag = 'white'
        self.other = 'white'
        self.fontDefault = 'black'

## what is a node?
class Nodes(object):
    def __init__(self):
        self.tasks = True
        self.tags = True
        self.projects = True
        self.annotations = True

## fine tune node existence and connection creation
class Excluded(object):
    def __init__(self):
        self.tags = [] # those nodes are supressed
        self.taskStatus = ['deleted'] # nodes removed
        self.taggedTaskStatus = set(['deleted']) # connection between tags and those are supressed
        self.annotationStatus = ['deleted', 'completed']
        # excluded tasks do not need connections

## edges weight
class Weights(object):
    def __init__(self):
        self.task2task = 31
        self.task2tag  = 1
        self.task2project = 5
        self.task2annotation = 99


class Conf(object):
    def __init__(self):
        self.filename = 'dotwarrior.svg'
        self.layout = "twopi"
        self.colors = Colors()
        self.weights = Weights()
        self.misc = Miscs()
        self.excluded = Excluded()
        self.nodes = Nodes()
