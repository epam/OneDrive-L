""" Common functionality for command parser
"""
import argparse


class SubParserHelpFormatter(argparse.RawDescriptionHelpFormatter):
    def _format_action(self, action):
        """
        Handles sub commands
        :param action:
        :return:
        """
        s_class = super(argparse.RawDescriptionHelpFormatter, self)
        parts = s_class._format_action(action)

        if action.nargs == argparse.PARSER:
            parts = "\n".join(parts.split("\n")[1:])

        return parts
