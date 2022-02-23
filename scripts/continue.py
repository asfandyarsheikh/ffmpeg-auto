#!/usr/bin/python

import sys

from ._ffutil import get_workdir, flush_toilet
from ._transcode import combine, encode

"""Sometimes encoding does not go as planned and the program exits. It is waste of time to restart
the encoding process from the beginning. This script converts videos in the supplied/input directory 
into a single video in the output directory

index supplied as first argument
path (optional) supplied as second argument
"""

idx, path = sys.argv[1:]
if not idx:
    raise Exception("Sorry, index is required")

workdir = path if path else get_workdir()
encode(workdir, int(idx))
combine(workdir)
flush_toilet(workdir)
