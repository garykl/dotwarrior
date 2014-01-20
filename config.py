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

from configtemplate import Conf

default = Conf()

mydefault = Conf()
mydefault.filename = 'mydefault'
mydefault.layout = 'neato' # circo seems to be slow, but stable
mydefault.excluded.tags = ['program']
mydefault.excluded.taggedTaskStatus = ['deleted', 'completed']
mydefault.excluded.taskStatus = ['deleted', 'completed']
mydefault.excluded.annotationStatus = ['completed']

tagWeight = Conf()
tagWeight.filename = 'tagWeight'
tagWeight.layout = 'neato'
tagWeight.excluded.taskStatus = ['deleted', 'completed']
tagWeight.excluded.taggedTaskStatus = ['deleted', 'completed']
tagWeight.excluded.tags = ['MPI']
tagWeight.nodes.projects = False
tagWeight.nodes.annotations = True
tagWeight.weights.task2tag = 70

oneProject = Conf()
oneProject.filename = 'oneProject'
oneProject.layout = 'neato'
oneProject.excluded.taskStatus = ['deleted', 'completed']
oneProject.excluded.taggedTaskStatus = ['deleted', 'completed']
oneProject.excluded.tags = ['MPI']
oneProject.nodes.projects = False
oneProject.nodes.annotations = True
oneProject.weights.task2tag = 20

noprojects = Conf()
noprojects.filename = 'noproject'
noprojects.layout = 'neato'
noprojects.nodes.projects = False
noprojects.excluded.tags = ['program']
noprojects.nodes.annotations = False
noprojects.weights.task2tag = 20


configs = {'tag': tagWeight,
           'one': oneProject,
           'df': default,
           '': mydefault,
           'np': noprojects}

