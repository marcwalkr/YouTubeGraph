"""
YouTubeGraph

Reads mobile screenshots of the Time watched page in YouTube using OCR and estimates bar graph values

Usage:
  youtubegraph <screenshot_image_path>

Options:
  <screenshot_image_path>     Path to YouTube Time watched page mobile screenshot
  -h --help                   Show this screen.
"""

import sys
from . import youtubegraph, helpers


def main():
    if len(sys.argv) < 2 or sys.argv[1] in ['-h', '--help']:
        print(__doc__)
        sys.exit(1)

    graph = youtubegraph.estimate(sys.argv[1])

    helpers.print_dictionary(graph)


if __name__ == '__main__':
    main()
