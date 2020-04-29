import tensorflow as tf
import ntpath


def get_frozen_graph(graph_file):
    """Read Frozen Graph file from disk."""
    with tf.gfile.FastGFile(graph_file, "rb") as f:
        graph_def = tf.GraphDef()
        graph_def.ParseFromString(f.read())
    return graph_def


def path_leaf(path):
    head, tail = ntpath.split(path)
    return tail or ntpath.basename(head)