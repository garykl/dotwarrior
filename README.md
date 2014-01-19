# dotwarrior

dotwarrior is glueing software, mainly, which connect the command line task
manager utility *taskwarrior* and the network visualising toolkit *graphviz*
to produce meaningful bullet lists.

## usage

You can call dotwarrior from the command line with the same filter options that
can be past to taskwarrior.


After setting up ...

$> ln -s /path/to/dotwarrior.py /path/inside/$PATH/dotwarrior  # and

$> chmod u+x /path/to/dotwarrior.py

$> mkdir ~/.dotwarrior


... dotwarrior can be called

$> dotwarrior

$> dotwarrior project:Presentation

$> dotwarrior +work


These commands ask taskwarrior for data, which is then transformed and
past to the dot program.

The default location for produced images is ~/.dotwarrior
The image file type is SVG.
