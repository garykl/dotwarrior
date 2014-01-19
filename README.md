# dotwarrior

dotwarrior is glueing software, which connect the command line task
manager utility `taskwarrior` with the network visualising toolkit `graphviz`
to produce meaningful bullet lists.

There are four different types of nodes considered:

1. task
2. tag
3. project
4. annotation

It's to a large extent customizable, which nodes to show and which not.

There will be five different types of connections considered:

1. task - task
2. task - tag
3. task - annotation
4. task - project
5. tag - project is planned

whose visiblity can be configured and the strength of the effect on the nodes
it is connected to, which, carefully used, enhances clear view.

dotwarrior is written in `python3`.

## usage

You can call `dotwarrior` from the command line with the same filter options that
can be passed to `taskwarrior`.


After setting up ...

    $> ln -s /path/to/dotwarrior.py /path/inside/$PATH/dotwarrior
    $> chmod u+x /path/to/dotwarrior.py
    $> mkdir ~/.dotwarrior  # place for saving images


... dotwarrior can be called

    $> dotwarrior
    $> dotwarrior project:Presentation
    $> dotwarrior +work


These commands ask `taskwarrior` for data, which is then transformed and
past to the `dot` program.

The default location for produced images is ~/.dotwarrior
The image file type is SVG.

## configuration

configuration is done in `python3`.

One or more configuration objects (configtemplate.Conf) can be instantiated,
and dynamically chosen at run-time through configurable command line arguments.

An example configuration is given in `config.py`.

The following paragraphs provide an overview over the options. It's probably
a good idea to read `configtemplate.py` parallel to the following.

### colors
different colors for different status of tasks can be / are set, like
completed, pending, deleted, ...
being a tag, a project, ...

### nodes
which nodes shall be shown? `True` means show, `False` mean don't show.

### excluded
exclude all tasks of a certain tag, all connections from deleted or completed
tasks or neglect all annotation of them.

### weights
how strong are the different kinds of nodes connected by their edges?
values should be greater than zero. Small values mean weak connections, large
values lead to string attraction.

### misc
The layout is one of the possible programs of the graphvis library, e.g.:
dot, neato, circle, fdp, sfdp, ...
filename, penwidth, characters per line, ...

### command line options
The keys in `configs` can be used as command line options by prefixing `--`.
If such an option is given, the corresponding value of `configs` is used.
If multiple options are given, one image for option is created.

## examples

The file `config.py` contains an example of a configuration described above.
Default values can be found in `configtemplate.py`.

The folder examples contain three images with the call

    $> dotwarrior project:dotwarrior

with slightly different settings and different layouts.
