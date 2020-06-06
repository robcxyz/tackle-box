# -*- coding: utf-8 -*-

"""Functions for generating a project from a project template."""
from __future__ import unicode_literals
from __future__ import print_function

import sys
import logging

# import shlex

from cookiecutter.operators import BaseOperator
import subprocess

logger = logging.getLogger(__name__)


class CommandOperator(BaseOperator):
    """Operator for PyInquirer type prompts."""

    type = 'command'

    def __init__(self, operator_dict, context=None, no_input=False):
        """Initialize PyInquirer Hook."""  # noqa
        super(CommandOperator, self).__init__(
            operator_dict=operator_dict, context=context, no_input=no_input
        )
        self.post_gen_operator = (
            self.operator_dict['delay'] if 'delay' in self.operator_dict else True
        )
        self.post_gen_operator = True

    def execute(self):
        """Run the prompt."""  # noqa
        p = subprocess.Popen(
            self.operator_dict['command'],
            shell=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
        )
        output, err = p.communicate()

        if err:
            sys.exit(err)

        a = output.decode("utf-8")
        print(a)
        return a
        # return output.decode("utf-8")


# class CommandInputOperator(BaseOperator):
#     """Operator for PyInquirer type prompts."""
#
#     type = 'command_input'
#
#     def __init__(self, operator_dict, context=None):
#         """Initialize PyInquirer Hook."""  # noqa
#         super(CommandInputOperator, self).__init__(
#             operator_dict=operator_dict, context=context
#         )
#         self.post_gen_operator = True
#
#     def execute(self):
#         """Run the prompt."""  # noqa
#         p = subprocess.Popen(
#             self.operator_dict['command'],
#             shell=True,
#             stdout=subprocess.PIPE,
#             stderr=subprocess.PIPE,
#         )
#         output, err = p.communicate()
#
#         if err:
#             sys.exit(err)
#
#         return output.decode("utf-8")
