import json
from subprocess import Popen, PIPE

def taskwarrior(cmd):
    'call taskwarrior, returning output and error'
    tw = Popen(['task'] + cmd.split(), stdout=PIPE, stderr=PIPE)
    return tw.communicate()


def taskwarriorJSON(query):
    'call taskwarrior, returning objects from json'
    JSON_START = '['
    JSON_END = ']'
    result, err = taskwarrior('export %s' % query)
    return json.loads(JSON_START + result.decode('utf8') + JSON_END)


def dot(instruction):
    'call dot, returning stdout and stdout'
    dot = Popen('dot -T svg'.split(), stdout=PIPE, stderr=PIPE, stdin=PIPE)
    return dot.communicate(instruction.encode())

