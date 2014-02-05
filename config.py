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

tagHierarchy = {'topic': ['swimmer', 'dissipation', 'flowfield', 'multipole'],
                'multipole': ['dipole', 'quadrupole', 'octupole'],
                'action': ['implement', 'maintain', 'plot', 'test',
                'analyse', 'decide', 'consider'],
                'who': ['janine', 'alex', 'thomas']}

default = Conf()

mydefault = Conf()
mydefault.layout = 'neato' # circo seems to be slow, but stable
mydefault.excluded.tags = ['program']
mydefault.excluded.taggedTaskStatus = ['deleted', 'completed']
mydefault.excluded.taskStatus = ['deleted', 'completed']
mydefault.excluded.annotationStatus = ['completed']

tagWeight = Conf()
tagWeight.layout = 'neato'
tagWeight.excluded.taskStatus = ['deleted', 'completed']
tagWeight.excluded.taggedTaskStatus = ['deleted', 'completed']
tagWeight.excluded.tags = ['MPI']
tagWeight.nodes.projects = False
tagWeight.nodes.annotations = True
tagWeight.weights.task2tag = 70

fewProjects = Conf()
fewProjects.layout = 'neato'
fewProjects.excluded.taskStatus = ['deleted', 'completed']
fewProjects.excluded.taggedTaskStatus = ['deleted', 'completed']
fewProjects.excluded.tags = ['MPI']
fewProjects.nodes.projects = True
fewProjects.nodes.annotations = True
fewProjects.weights.task2tag = 20

oneProject = Conf()
oneProject.layout = 'neato'
oneProject.excluded.taskStatus = ['deleted', 'completed']
oneProject.excluded.taggedTaskStatus = ['deleted', 'completed']
oneProject.excluded.tags = ['MPI']
oneProject.nodes.projects = False
oneProject.nodes.annotations = True
oneProject.weights.task2tag = 20

noprojects = Conf()
noprojects.layout = 'neato'
noprojects.nodes.projects = False
noprojects.excluded.tags = ['program']
noprojects.nodes.annotations = False
noprojects.weights.task2tag = 20

notasks = Conf()
notasks.layout = 'neato'
notasks.nodes.tasks = False
notasks.nodes.annotations = False
notasks.edges.projectVStags = True
notasks.excluded.tags = []
notasks.nodes.annotations = False
notasks.weights.task2tag = 20

tagtag = Conf()
tagtag.layout = 'neato'
tagtag.nodes.tasks = False
tagtag.nodes.projects = False
tagtag.nodes.annotations = False
tagtag.edges.tagVStags = True
tagtag.excluded.tags = []
tagtag.nodes.annotations = False
tagtag.weights.task2tag = 20

urgency = Conf()
urgency.layout = 'neato'
urgency.colors.byUrgency = True
urgency.excluded.tags = ['MPI']
urgency.tagHierarchy = tagHierarchy
urgency.nodes.annotations = False
urgency.weights.task2tag = 2


configs = {'tag': tagWeight,
           'nt': notasks,
           'tt': tagtag,
           'few': fewProjects,
           'one': oneProject,
           'urg': urgency,
           'df': default,
           '': mydefault,
           'np': noprojects}

