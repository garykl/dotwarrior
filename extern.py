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

import json
import sys
from subprocess import Popen, PIPE


## helper
def splitList(fn, ll):
    """
    split list.
    fn applied to an element of ll returns either True or False.
    return a tuple with a list of =True= elements left and list
    of =False= elemtns right.
    """
    left = []
    right = []
    for l in ll:
        if fn(l):
            left.append(l)
        else:
            right.append(l)
    return (left, right)


def interpreteInput(args):
    """
    input can be ...
    ... a filename, preceded with '-'
    ... a configuration key, preceded with '--'
    """
    def isConf(a):
        return '--' in a
    (confOptions, otherOptions) = splitList(isConf, args)
    confKeys = list(map(lambda x: x[2:], confOptions)) # cut the leading --
                                                       # for each key, although
                                                       # we only need one!
    def isFile(s):
        return '-' in s
    (optionKey, optionValue) = splitList(isFile, otherOptions) # so far there
    filename = optionValue[0]                                  # can only be one file
    if len(confKeys) == 0:
        confKeys = ['']

    return (filename, confKeys[0])


def taskwarrior(cmd):
    'call taskwarrior, returning output and error'
    tw = Popen(['task'] + cmd.split(), stdout=PIPE, stderr=PIPE)
    return tw.communicate()


def taskwarriorJSON():
    """
    read input from taskwarrior via stdin,
    return list of dictionaries.
    """
    taskwarrioroutput = sys.stdin.read()
    return json.loads('[' + taskwarrioroutput + "]")


def dot(conf, instruction, filename):
    'call dot, returning stdout and stdout'
    svgViewer = "eog"
    dot = Popen('dot -T svg'.split(), stdout=PIPE, stderr=PIPE, stdin=PIPE)
    (png, err) = dot.communicate(instruction.encode())
    if err != b'':
        print ('Error calling dot:')
        print (err.strip())
    else:
        with open('{0}.svg'.format(filename), 'w') as f:
            f.write(png.decode('utf-8'))
            print(svgViewer + " " + filename + ".svg &")


