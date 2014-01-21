# dotwarrior

dotwarrior is glueing software, which connect the command line task
manager utility `taskwarrior` with the network visualising toolkit `graphviz`
to produce meaningful bullet lists in the form of a graph.

There are four different types of nodes considered:

1. task
2. tag
3. project
4. annotation

It's to a large extent customizable, which nodes to show and which not and
how they look like.

There will be five different types of connections:

1. task - task
2. task - tag
3. task - annotation
4. task - project
5. tag - project is planned

whose visiblity can be configured and the strength of the effect on the nodes
it is connected to, which, carefully used, enhances clear view.

dotwarrior is written in `python3`, but works with `python2` as well.

## usage

After setting up ...

    $> ln -s /path/to/dotwarrior.py /path/inside/$PATH/dotwarrior
    $> chmod u+x /path/to/dotwarrior.py
    $> mkdir ~/.dotwarrior  # place for saving images


... dotwarrior can be called

    $> taskwarrior export | dotwarrior out
    $> taskwarrior export project:Presentation | dotwarrior presi
    $> taskwarrior export +work | dotwarrior constr

An argument without a dash is interpeted as filename, which means, we just
created three files out.svg, presi.svg and constr.svg. More possible
output formats will follow.

Note, that taskwarrior must be invoked with the export option, the output
data in JSON format, is piped into dotwarrior. As a consequence,
the full power of taskwarrior is conserved as it is.

## configuration

configuration is done in `python3`, but the plan is to read from a configuration
file.

One or more configuration objects (configtemplate.Conf) are instantiated, one
of them is dynamically chosen at run-time through configurable command
line arguments.

Several example configurations are given in `config.py`.

The following paragraphs provide an overview over the planned and partly
realized configuration options. It's probably
a good idea to read `configtemplate.py` in parallel to the following.

### colors
different colors for different status of tasks can be / are set, like
completed, pending, deleted or being a tag, a project, ...

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

    $> taskwarrior export project:dotwarrior | dotwarrior

with slightly different settings and different layouts.

## How could I

This project was a spontaneous effect, inspired and build out of
[graphdeps](http://pastebin.com/9EyvEL0M/ "Graphdeps"), after finding
the inspiring taskwarrior.
