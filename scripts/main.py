#!/usr/bin/python

from ._transcode import encode, combine
from ._ffutil import get_workdir, flush_toilet

"""Converts videos in the input directory into a single video in the output directory"""

def process():
    flush_toilet()
    workdir = get_workdir()
    encode(workdir)
    combine(workdir)
    flush_toilet(workdir)
    process()


process()
