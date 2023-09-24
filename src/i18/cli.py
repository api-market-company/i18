import argparse
import logging
import sys

from i18 import __version__, apply_i18
import json


__author__ = "sanchezcarlosjr"
__copyright__ = "sanchezcarlosjr"
__license__ = "MIT"

_logger = logging.getLogger(__name__)


class TranslateAction(argparse.Action):
    def __call__(self, parser, namespace, files, option_string=None):
        _logger.debug("Starting...")
        for file in files:
            try:
                new_text,translations = apply_i18(file.read())
            except Exception as e:
                raise Exception(f"In file {file.name} has ocurred an error: {str(e)}")
            if namespace.save and translations != {'es': {}, 'en': {}}:
               with open(file.name, 'w') as writer:
                   writer.write(new_text)
            print(json.dumps(translations))
        _logger.debug("Ending...")

# ---- CLI ----
# The functions defined in this section are wrappers around the main Python
# API allowing them to be called directly from the terminal as a CLI
# executable/script.


def parse_args(args):
    """Parse command line parameters

    Args:
      args (List[str]): command line parameters as list of strings
          (for example  ``["--help"]``).

    Returns:
      :obj:`argparse.Namespace`: command line parameters namespace
    """
    parser = argparse.ArgumentParser(description="Transform into i18 based on a grammar")
    parser.add_argument(
        "--version",
        action="version",
        version=f"i18 {__version__}",
    )
    parser.add_argument(
            dest="infile",
            help="file paths",
            nargs="+",
            action=TranslateAction,
            type=argparse.FileType('r'),
            default=sys.stdin
    )
    parser.add_argument(
            "-g",
            "--grammar",
            dest="grammar",
            help="file grammar",
            nargs="?",
            type=argparse.FileType('r'),
    )
    parser.add_argument(
            "-s",
            "--save",
            dest="save",
            help="Write changes in file",
            action="store_true"
    )
    parser.add_argument(
        "-v",
        "--verbose",
        dest="loglevel",
        help="set loglevel to INFO",
        action="store_const",
        const=logging.INFO,
    )
    parser.add_argument(
        "-vv",
        "--very-verbose",
        dest="loglevel",
        help="set loglevel to DEBUG",
        action="store_const",
        const=logging.DEBUG,
    )
    return parser.parse_args(args)


def setup_logging(loglevel):
    """Setup basic logging

    Args:
      loglevel (int): minimum loglevel for emitting messages
    """
    logformat = "[%(asctime)s] %(levelname)s:%(name)s:%(message)s"
    logging.basicConfig(
        level=loglevel, stream=sys.stdout, format=logformat, datefmt="%Y-%m-%d %H:%M:%S"
    )


def main(args):
    """Wrapper allowing :func:`fib` to be called with string arguments in a CLI fashion

    Instead of returning the value from :func:`fib`, it prints the result to the
    ``stdout`` in a nicely formatted message.

    Args:
      args (List[str]): command line parameters as list of strings
          (for example  ``["--verbose", "42"]``).
    """
    args = parse_args(args)
    setup_logging(args.loglevel)


def run():
    """Calls :func:`main` passing the CLI arguments extracted from :obj:`sys.argv`

    This function can be used as entry point to create console scripts with setuptools.
    """
    main(sys.argv[1:])


if __name__ == "__main__":
    run()
