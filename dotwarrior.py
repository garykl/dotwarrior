#!/usr/bin/env python3
#
#
# Copright 2014 Gary Klindt
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

import sys

from extern import interpreteInput, dot, taskwarriorJSON
from dotter import dotsource, connector, nodes
from validate import TaskwarriorExploit
from config import configs


def prog(conf, tasks):
    """
    (i)   prepare data
    (ii)  data to string
    (iii) call dot
    """

    taskwarriordata = TaskwarriorExploit(tasks, conf.excluded)

    def graph(c, ts):
        return (nodes(c, ts), connector(c, ts))

    (nods, connects) = graph(conf, taskwarriordata)
    dotSource = dotsource(conf, nods, connects)

    dot(conf, dotSource)


confKeys = interpreteInput(sys.argv[1:])

tasks = taskwarriorJSON()
for conf in [configs[c] for c in confKeys]:
    prog(conf, tasks)
