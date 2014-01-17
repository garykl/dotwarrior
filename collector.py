def excludeElementsFrom(toExclude, ll):
    """
    toExclude and ll are lists of elements.
    return a new list, containing all elements of ll,
    which are not in toExclude.
    """
    res = []
    for l in ll:
        if not l in toExclude:
            res.append(l)
    return res


class Collector(object):

    def __init__(self, tasks, excludedTags):
        self.tasks = tasks
        self.projects = self.projects()
        self.tags = excludeElementsFrom(excludedTags, self.tags())
        self.uuids = self.uuids()

    def projects(self):
        res = set()
        for task in self.tasks:
            if 'project' in task.keys():
                res.add(task['project'])
        return res

    def tags(self):
        """
        data is list of dictionaries, containing data from
        the export function of taskwarrior.
        return a set with the keys.
        """
        allTags = set()
        for task in self.tasks:
            if 'tags' in task.keys():
                for tag in task['tags']:
                    if tag not in allTags:
                        allTags.add(tag)
        return allTags

    def uuids(self):
        res = []
        for task in self.tasks:
            res.append(task['uuid'])
        return res


