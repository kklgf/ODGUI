import tensorflow as tf
import ntpath
import subprocess
import shlex
import json


def get_frozen_graph(graph_file):
    """Read Frozen Graph file from disk."""
    with tf.gfile.FastGFile(graph_file, "rb") as f:
        graph_def = tf.GraphDef()
        graph_def.ParseFromString(f.read())
    return graph_def


def video_metadata(video_path):
    cmd = "ffprobe -v quiet -print_format json -show_streams"
    args = shlex.split(cmd)
    args.append(video_path)
    # run the ffprobe process, decode stdout into utf-8 & convert to JSON
    ffprobeOutput = subprocess.check_output(args).decode('utf-8')
    ffprobeOutput = json.loads(ffprobeOutput)
    return ffprobeOutput['streams'][0]


def path_leaf(path):
    head, tail = ntpath.split(path)
    return tail or ntpath.basename(head)
