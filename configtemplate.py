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
        self.byUrgency = False
        self.byEntry = False

## what is a node?
class Nodes(object):
    def __init__(self):
        self.tasks = True
        self.tags = True
        self.projects = True
        self.annotations = True

class Edges(object):
    def __init__(self):
        self.tagVStags = False
        self.projectVStags = False

## fine tune node existence and connection creation
class Excluded(object):
    def __init__(self):
        self.tags = [] # those nodes are supressed
        self.taskStatus = ['deleted'] # nodes removed
        self.taggedTaskStatus = set(['deleted']) # connection between tags and those are supressed
        self.annotationStatus = ['deleted', 'completed']

## edges weight
class Weights(object):
    def __init__(self):
        self.task2task = 0.3
        self.task2tag  = 0.1
        self.task2project = 0.1
        self.task2annotation = 0.9
        self.project2tag = 0.1
        self.tag2tag = 0.1
        self.tagHierarchy = 0.2


class Conf(object):
    def __init__(self):
        self.layout = "twopi"
        self.colors = Colors()
        self.weights = Weights()
        self.misc = Miscs()
        self.excluded = Excluded()
        self.nodes = Nodes()
        self.edges = Edges()
        self.tagHierarchy = {}
