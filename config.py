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

from configtemplate import Conf, WarriorSetting

default = Conf()

mydefault = Conf()
mydefault.filename = 'mydefault'
mydefault.excluded.tags = ['program', 'MPI']
mydefault.excluded.taggedTaskStatus = ['deleted', 'completed']
mydefault.excluded.taskStatus = ['deleted', 'completed']
mydefault.excluded.annotationStatus = ['completed']

noprojects = Conf()
noprojects.filename = 'noproject'
noprojects.nodes.projects = False
noprojects.excluded.tags = ['program']
noprojects.weights.task2tag = 20


configs = {'df': default,
           '': mydefault,
           'np': noprojects}

registeredLists = [WarriorSetting(['pro:GroupRetreat2014'],
                                  mydefault,
                                  filename='groupretreat'),
                   WarriorSetting(['+MPI'],
                                  mydefault,
                                  filename='work'),
                   WarriorSetting([''],
                                  noprojects,
                                  filename='global')]
