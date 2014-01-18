import json
from subprocess import Popen, PIPE


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
    def fun(a):
        return '--' in a
    (confOptions, taskwarriorArgs) = splitList(fun, args)
    confKeys = list(map(lambda x: x[2:], confOptions)) # cut the leading --
    if len(confKeys) == 0:
        confKeys = ['']
    return (confKeys, taskwarriorArgs)


def taskwarrior(cmd):
    'call taskwarrior, returning output and error'
    tw = Popen(['task'] + cmd.split(), stdout=PIPE, stderr=PIPE)
    return tw.communicate()


def taskwarriorJSON(options):
    'call taskwarrior, returning objects from json'
    JSON_START = '['
    JSON_END = ']'
    query = ' '.join(options)
    result, err = taskwarrior('export %s' % query)
    return json.loads(JSON_START + result.decode('utf8') + JSON_END)


def dot(conf, instruction):
    'call dot, returning stdout and stdout'
    dot = Popen('dot -T svg'.split(), stdout=PIPE, stderr=PIPE, stdin=PIPE)
    (png, err) = dot.communicate(instruction.encode())
    if err != b'':
        print ('Error calling dot:')
        print (err.strip())
    else:
        with open('{0}.svg'.format(conf.filename), 'w') as f:
            f.write(png.decode('utf-8'))


