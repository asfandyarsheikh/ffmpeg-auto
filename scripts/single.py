#!/usr/bin/python

import os

from ._ffutil import list_files
from ._transcode import process_encode
from ._varlist import singlepath


def encode_single():
    """Converts mp4 in 'single' folder to mkv and removes the original file"""
    lst = list_files(singlepath, ("mp4",), False)
    for val in lst:
        name = val.split("/")[-1]
        name = name.split(".")
        name[-1] = ".mkv"
        name = ".".join(name)
        outpath = singlepath + "/" + name
        process_encode(val, outpath)
        os.remove(val)


encode_single()
