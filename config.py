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

tagHierarchy = {}#'topic': ['swimmer', 'fluctuation', 'dissipation', 'flowfield', 'multipole'],
                # 'multipole': ['dipole', 'quadrupole', 'octupole'],
                # 'action': ['implement', 'maintain', 'plot', 'test',
                # 'analyse', 'bugfix', 'decide', 'consider', 'ask', 'answer'],
                # 'who': ['janine', 'alex', 'thomas']}

default = Conf()

oneTag = Conf()
oneTag.layout = 'fdp'
oneTag.colors.byEntry = True
oneTag.nodes.projects = True
oneTag.nodes.annotations = True
oneTag.excluded.tags = []

oneProject = Conf()
oneProject.layout = 'neato'
oneProject.colors.byEntry = True
oneProject.nodes.projects = False
oneProject.nodes.annotations = True
oneProject.tagHierarchy = tagHierarchy

oneBigProject = Conf()
oneBigProject.layout = 'fdp'
oneBigProject.colors.byEntry = True
oneBigProject.nodes.projects = True
oneBigProject.nodes.annotations = True
# oneBigProject.tagHierarchy = tagHierarchy
oneBigProject.excluded.projects = ['phd']
oneBigProject.weights.project2tag = 0.00001
oneBigProject.weights.tag2tag = 0.1
oneBigProject.weights.task2tag = 0.1

notasks = Conf()
notasks.layout = 'fdp'
notasks.nodes.tasks = False
notasks.nodes.annotations = False
notasks.edges.projectVStags = True
notasks.excluded.tags = []
notasks.nodes.annotations = False
notasks.weights.task2tag = 20

tagtag = Conf()
tagtag.layout = 'fdp'
tagtag.nodes.tasks = False
tagtag.nodes.projects = False
tagtag.nodes.annotations = False
tagtag.edges.tagVStags = True
tagtag.excluded.tags = []
tagtag.nodes.annotations = False
tagtag.tagHierarchy = tagHierarchy
tagtag.weights.task2tag = 20

urgency = Conf()
urgency.layout = 'fdp'
urgency.colors.byUrgency = True
urgency.tagHierarchy = tagHierarchy
urgency.nodes.annotations = False
urgency.weights.task2tag = 2

entry = Conf()
entry.layout = 'fdp'
entry.colors.byEntry = True
entry.tagHierarchy = tagHierarchy
entry.nodes.annotations = True

configs = {'nt': notasks,
           'tt': tagtag,
           'project': oneProject,
           'bigproject': oneBigProject,
           'tag': oneTag,
           'urg': urgency,
           '': entry,
           'df': default }

