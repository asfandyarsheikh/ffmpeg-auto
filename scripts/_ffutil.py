import glob
import os
import re
import shutil

from ._varlist import inputpath, temppath, mp4_list


def natural_sort(inp):
    """Sorts a list of strings in natural order 1, 2, 3 instead of 1, 10, 11

    Args:
        inp (list(str)): The list of file path strings

    Returns:
        list(str): a list of file path strings in natural alphabetical order
    """
    convert = lambda text: int(text) if text.isdigit() else text.lower()
    alphanum_key = lambda key: [convert(c) for c in re.split('([0-9]+)', key)]
    return sorted(inp, key=alphanum_key)


def list_files(path, exts=("mp4", "mkv"), rec=True):
    """Crawls directory and lists paths of all file with given extensions in alphabetical order

    Args:
        path (str): The absolute path of the directory to crawl
        exts (tuple(str)): A tuple of file extensions
        rec (bool): Whether to crawl subdirectories

    Returns:
        list(str): a list of file path strings in natural alphabetical order
    """
    output = []
    for ext in exts:
        pathstr = ("/**/*." + ext) if rec else ("/*." + ext)
        output.extend(glob.glob(path + pathstr, recursive=rec))
    return natural_sort(output)


def clear_dir(path):
    """Clears directory

    Args:
        path (str): The absolute path of the directory to clear
    """
    files = glob.glob(path + '/*')
    for f in files:
        os.remove(f)


def remove_dir(path):
    """Removes directory

    Args:
        path (str): The absolute path of the directory to remove
    """
    shutil.rmtree(path)


def flush_toilet(path=None):
    """Clears temporary directory and removes workdir if provided

    Args:
        path (str): The absolute path of the work directory to remove after encoding is complete
    """
    clear_dir(temppath)
    if path:
        remove_dir(path)


def list_dir(path):
    """List directory

    Args:
        path (str): The absolute path of the directory to clear

    Returns:
        list(str): a list of directory paths ordered by time modified
    """
    files = glob.glob(path + "/*/")
    return sorted(files, key=lambda t: os.stat(t).st_mtime)


def count_files(idx=0):
    """Count files in directory on index

    Args:
        idx (int): The index of the directory in a list ordered by modification date

    Returns:
        int: number of files in the directory
    """
    return len(list_files(list_dir(inputpath)[idx]))


def get_workdir():
    """Chooses a subdirectory from the input folder

    Returns:
        str: absolute path of work directory
    """
    dirs = list_dir(inputpath)
    if len(dirs) <= 0:
        print("FINISHED!!!!!")
        return
    return dirs[0]


def save_list():
    """Writes a list to a file

    Returns:
        tuple(str, list(str)): a tuple of absolute path of text file and list of file path strings
    """
    lst = list_files(temppath, ("mkv",), False)
    with open(mp4_list, 'w') as f:
        for item in lst:
            f.write("file '%s'\n" % item)
    return mp4_list, lst
