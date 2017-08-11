""" Common functionality for command parser
"""
import argparse


class SubParserHelpFormatter(argparse.RawDescriptionHelpFormatter):
    """ Helper class to format action
    """

    def _format_action(self, action):
        """
        Handles sub commands
        :param action:
        :return:
        """
        fmt = super(argparse.RawDescriptionHelpFormatter, self)
        parts = fmt._format_action(action)  # pylint: disable=protected-access

        if action.nargs == argparse.PARSER:
            parts = '\n'.join(parts.split('\n')[1:])

        return parts
