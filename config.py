from configtemplate import Conf


## many configs are possible
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
noprojects.weights.task2tag = 5

configs = {'df': default,
           '': mydefault,
           'np': noprojects}
