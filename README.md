# dotwarrior

dotwarrior creates meaningful bullet lists in graph appearance.

Using the output of `taskwarrior export`, nice visualizations using
`graphviz` are produced. If you don't use taskwarrior, this program
won't make any sense to you, except you want to learn using it, which
could point out to be useful.

Some features, provided by dotwarrior, only make sense, when using taskwarrior
with a certain workflow. I use taskwarrior's tags intensively, for categorizing
tasks by topic, people that are affected, places, actions to be taken for
finishing a task, ...

The produced visualizations are a colorful graphs (mathematical for networks),
whose nodes (boxes with text in it) can be:

1. tasks
2. tags
3. projects
4. annotations

Edges (connections between nodes, represented as arrows) can be:

1. task - task
2. task - tag
3. task - annotation
4. task - project
5. tag - project
6. tags - tag

The configuration options are already extensive, but not fully developed.
Configuration is done in `python3`, which is the language, dotwarrior is
written in.

## usage

Dotwarrior is called as follows, if it is executable (file permission) and
in a folder inside the $PATH variable:

    $> taskwarrior export | dotwarrior.py out
    $> taskwarrior export project:presentation | dotwarrior.py presi
    $> taskwarrior export +work | dotwarrior.py constr

An argument without a dash is interpeted as filename, which means, we just
created three files out.svg, presi.svg and constr.svg. More possible
output formats will follow.

Note, that taskwarrior must be invoked with the export option, which produces
data in JSON format, that is piped into dotwarrior. As a consequence,
the full power of taskwarrior is conserved as it is.

dotwarrior is only useful, if you fine tune your own configurations. An
arbitrary number of configurations can be created (it is an instance of the
configuration class `Conf`) and then be used by specifying command line options.
See also section configuration/command line options.

## configuration

Configuration is done in `python3`.

One or more configuration objects (configtemplate.Conf) are instantiated, one
of them is dynamically chosen at run-time through configurable command
line arguments (see section configuration/command line options).

Several example configurations are given in `config.py`.

The following paragraphs provide an overview over the planned and partly
realized configuration options. It's probably
a good idea to read `configtemplate.py` in parallel to the following.

For the following subsections, assume that there is an object

    conf = Conf()

### colors
different colors for different status of tasks can be / are set, like
completed, pending, deleted or being a tag or a project. The following options
are available, and its default values are shown. It is hopwfully self
explanatory.

- `conf.colors.project = 'white'`
- `conf.colors.annotation = 'yellow'`
- `conf.colors.blocked = 'green'`
- `conf.colors.unblocked = 'lightgreen'`
- `conf.colors.done = 'grey'`
- `conf.colors.wait = 'white'`
- `conf.colors.deleted = 'pink'`
- `conf.colors.tag = 'white'`
- `conf.colors.fillTag = 'black'`
- `conf.colors.fontTag = 'white'`
- `conf.colors.other = 'white'`
- `conf.colors.fontDefault = 'black'`
- `conf.colors.byUrgency = False`

Colors can also be HSV codes ('h,s,v', h, s and v being numbers between 0 and 1)
and RGB as hex code (e.g. '#00ff33').

The option `byUrgency` is special. If it is set to `True`, the default colors
for tasks are ignored. Instead, a color code is used for indicating the
urgency of a task, which is calculated by taskwarrior.

If option `byEntry` is set and `byUrgency` is not set, the task nodes are
colored by the date when they were created.

### layout
The layout is one of the possible programs of the graphvis library, e.g.:
dot, neato, circo, fdp, sfdp. Read `man dot` for more information.

### nodes
which nodes shall be shown? `True` means show, `False` mean don't show.
Self explanatory!

### edges
One can choose to show edges between certain tags by setting
`conf.edges.tagVStags = True`. This is only useful, when setting
`conf.nodes.tasks = False`, because the connections between different tags
are set, when one task has multiple tags. It shows
you information about your working style, like what kind of stuff are you doing
when working at certain places or with certain persons, or what are you really
doing when working on certain topics. This option is only
useful if you use tags extensively!

You can also set `conf.edges.projectVStags = True`, which, again, is only useful when
`conf.nodes.tasks = False`, since connection between a project and a tag is
drawn when a task in a project has that tag.

### excluded
those tags are supressed:
`conf.excluded.tags = []`

deleted tasks are not shown:
`conf.excluded.taskStatus = ['deleted']`

deleted tasks are not connected to tags:
`conf.excluded.taggedTaskStatus = set(['deleted'])`

deleted and completed tasks annotations are not shown:
`conf.excluded.annotationStatus = ['deleted', 'completed']`

### weights
how strong are the different kinds of nodes connected by their edges?
values should be greater than zero. Small values mean weak connections, large
values lead to strong attraction.

### misc
penwidth, characters per line.

### tag hierarchy
Setting `conf.tagHierarchy` to some dictionary builds up a tag hierarchy.
Entirely new tag symbols, which are not contained in your taskwarrior data,
can be used.

    conf.tagHierarchy = {'program': ['maintain', 'implement', 'test', 'refactor']

This would lead to connections between program with each of the elements in
the value list. Of course, many such key value pairs can be defined, and keys
can be used in the value list of other pairs, as well.

This proves useful not only for having a clearer view, but also
for having a better alignment relativ to certain actions or places, ...

This, again, is only useful when using tags extensively.

### command line options
The keys in `configs` can be used as command line options by prefixing `--`.
If such an option is given, the corresponding value of `configs` is used.

    task project:dotwarrior status:pending export | dotwarrior.py --urg out

creates a graph that is color coded by urgency, that means urgent tasks that
should be done at first are colored in red, whereas more unimportant tasks
are blue. It is saved in `out.svg`.

## examples

The file `config.py` contains many examples of configurations described above.
Default values can be found in `configtemplate.py`.

## How could I

This project was a spontaneous effect, build out of
[graphdeps](http://pastebin.com/9EyvEL0M/ "Graphdeps"), after finding
the inspiring taskwarrior.
