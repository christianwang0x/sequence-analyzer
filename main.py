#!/usr/bin/python3

from analyzer import *
import sys
import numpy as np
import matplotlib.pyplot as plt
from encoders import *

HELP_MSG = ('Encoders: base64, asciihex, binary, url\n'
            'python3 %s -i <input-file> -d [decoder]' % sys.argv[0])


# Convert the contents of a file to a sequence of bytes,
#   decoding the data accordingly.
# Data can be decoded from several formats
def get_sequence(file_pointer, encoding=None):
    lines = [l.strip() for l in file_pointer if l.strip()]
    if encoding == "base64":
        sequence = decode_list(lines, Base64)
    elif encoding == "asciihex":
        sequence = decode_list(lines, AsciiHex)
    elif encoding == "binary":
        sequence = decode_list(lines, Binary)
    elif encoding == "url":
        sequence = decode_list(lines, Url)
    elif encoding is None:
        sequence = decode_list(lines, Plain)
    else:
        e = EncoderException(BAD_ENCODER_MSG, [])
        raise e
    return sequence


# Analyze a 2d array of bytes so that correlation and
#   uniformity data can be returned
def analyze(sequence):
    max_line_len = max(map(len, sequence))
    output_data = []
    for index in range(max_line_len):
        c = Column(sequence, index)
        residual, uniformity = c()
        output_data.append((residual, uniformity))
    flipped_output = invert_residual_data(output_data)
    return flipped_output


# Present the data as a graph via matplotlib
def visualize(data):
    residuals, uniformities = zip(*data)
    n_groups = len(residuals)
    fig = plt.figure(1)
    fig.set_size_inches(10, 8)

    index = np.arange(n_groups)
    bar_width = 0.5
    opacity = 0.8

    plot_vals = ({"pos": 211, "color": "b",
                  "label": "Polynomial Correlation", "xlabel": "Byte Index",
                  "ylabel": "Correlation", "title": "Polynomial Correlation",
                  "dataset": residuals},
                 {"pos": 212, "color": "g",
                  "label": "Uniformity", "xlabel": "Byte Index",
                  "ylabel": "Uniformity", "title": "Uniformity",
                  "dataset": uniformities})
    for d in plot_vals:
        plt.subplot(d["pos"])
        plt.bar(index, d["dataset"], bar_width,
                alpha=opacity, color=d["color"],
                label=d["label"])
        plt.xlabel(d["xlabel"])
        plt.ylabel(d["ylabel"])
        plt.title(d["title"])
        plt.legend()
        plt.xticks(index, range(len(residuals)))
        plt.tight_layout()
    plt.show()


def main():
    input_file = ""
    decoder = None
    for idx, opt in enumerate(sys.argv):
        if opt == '-h':
            print(HELP_MSG)
            sys.exit()
        elif opt == "-i":
            input_file = sys.argv[idx+1]
        elif opt == "-d":
            decoder = sys.argv[idx+1]
        else:
            continue

    try:
        with open(input_file) as fp:
            sequence = get_sequence(fp, encoding=decoder)
            data = analyze(sequence)
            visualize(data)
            exit(0)
    except FileNotFoundError:
        print(HELP_MSG)
        exit(1)


if __name__ == '__main__':
    main()
