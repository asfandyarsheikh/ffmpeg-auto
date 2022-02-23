import ffmpeg

from ._ffutil import save_list, list_files
from ._varlist import ffconfig, temppath, outputpath


def get_streams(inp):
    """Reads input file and converts into ffmpeg streams

    Args:
        inp (str): The absolute path of the input file

    Returns:
        list(ffmpeg.stream): A list of video and/or audio streams
    """
    istream = ffmpeg.input(inp)
    streams = ffmpeg.probe(inp)["streams"]
    output = []
    for stream in streams:
        if stream["codec_type"] == "video":
            output.append(istream.video)
        if stream["codec_type"] == "audio":
            output.append(istream.audio)
    return output


def process_encode(inp, oup):
    """The actual encoding takes place here

    Args:
        inp (str): The absolute path of the input file
        oup (str): The absolute path of the output file
    """
    try:
        streams = get_streams(inp)
        stream = ffmpeg.output(*streams, oup, **ffconfig).overwrite_output()
        ffmpeg.run(stream)
    except ffmpeg.Error as e:
        print(e)


def process_combine(inp, oup):
    """Concatenates all video files listed in a text file into a single mkv

    Args:
        inp (str): The absolute path of the text file containing mp4 list
        oup (str): The absolute path of the output file
    """
    try:
        stream = ffmpeg.input(inp, format='concat', safe=0)
        stream = ffmpeg.output(stream, oup, c='copy').overwrite_output()
        ffmpeg.run(stream)
    except ffmpeg.Error as e:
        print(e)


def encode(workdir, ix=0):
    """Encodes all video files in workdir to mkv files in temp directory

    Args:
        workdir (str): The absolute path of the work directory
        ix (int): The index to continue encoding from
    """
    lst = list_files(workdir)[ix:]
    for idx, val in enumerate(lst):
        outpath = temppath + "/" + str(idx + ix) + ".mkv"
        process_encode(val, outpath)


def combine(workdir):
    """Concatenates all video files in temp directory to a single mkv file in output directory

    Args:
        workdir (str): The absolute path of the work directory used as the name of final mkv
    """
    (mp4_list,) = save_list()
    combinedfile = outputpath + "/" + workdir.split("/")[-2] + ".mkv"
    process_combine(mp4_list, combinedfile)
