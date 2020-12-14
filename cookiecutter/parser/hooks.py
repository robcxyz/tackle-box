# -*- coding: utf-8 -*-

"""Functions for discovering and executing various cookiecutter operators."""
from __future__ import print_function
import logging
from PyInquirer import prompt
from pydantic.error_wrappers import ValidationError

from cookiecutter.render import render_variable
from cookiecutter.parser.providers import get_hook
from cookiecutter.utils.conditionals import evaluate_when
from cookiecutter.exceptions import HookCallException
from cookiecutter.models import BaseHook

from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from cookiecutter.models import Mode, Context, Source

logger = logging.getLogger(__name__)

KEYWORDS = {'when', 'loop', 'chdir' 'existing_context', ''}


def run_operator(context: 'Context', mode: 'Mode'):
    """Run operator."""
    if context.input_dict is None:
        context.input_dict = {}

    Hook = get_hook(context.hook_dict['type'], context)

    try:
        # Take the items out of the global context and mode if they are
        # declared in the hook dict.
        exclude_context = {
            i for i in context.dict().keys() if i in context.hook_dict.keys()
        }
        exclude_context.update({'env'})
        exclude_mode = {i for i in mode.dict().keys() if i in context.hook_dict.keys()}
        exclude_mode = exclude_mode if exclude_mode != set() else {'tmp'}

        if 'no_input' in context.hook_dict:
            print()

        hook = Hook(
            **context.hook_dict,
            **context.dict(exclude=exclude_context),
            **mode.dict(exclude=exclude_mode),
        )
    except ValidationError as e:
        if 'extra fields not permitted' in e.__repr__():
            # This is very common and so lets enrich the error to give the user
            # more context. Return all the fields in the hook by removing all the
            # base fields.
            fields = '--> ' + ', '.join(
                [
                    i
                    for i in Hook().dict().keys()
                    if i not in BaseHook().dict().keys() and i != 'type'
                ]
            )
            error_out = (
                f"Error: The field \"{e.raw_errors[0]._loc}\" is not permitted in "
                f"key=\"{context.key}\".\n"
                f"Only values accepted are {fields}, plus base fields --> "
                f"type, when, loop, chdir."
            )
            raise HookCallException(error_out)
        else:
            raise e

    if hook.post_gen_operator:
        return None, hook
    else:
        return hook.call(), None


def parse_hook(
    context: 'Context', mode: 'Mode', s: 'Source', append_key: bool = False,
):
    """Parse input dict for loop and when logic and calls hooks.

    :return: cc_dict
    """
    if not context.context_key:
        context.context_key = next(iter(context.input_dict))  # TODO -> wtf

    logger.debug("Parsing context_key: %s and key: %s" %
                 (context.context_key, context.key))
    context.hook_dict = context.input_dict[context.context_key][context.key]

    when_condition = evaluate_when(context.hook_dict, context)

    if when_condition:
        # Extract loop
        if 'loop' in context.hook_dict:
            loop_targets = render_variable(context, context.hook_dict['loop'])
            context.hook_dict.pop('loop')

            loop_output = []
            for i, l in enumerate(loop_targets):
                context.output_dict.update({'index': i, 'item': l})
                loop_output += [parse_hook(context, mode, s, append_key=True)]

            context.output_dict.pop('item')
            context.output_dict.pop('index')
            context.output_dict[context.key] = loop_output
            return context.output_dict

        if 'block' not in context.hook_dict['type']:
            context.hook_dict = render_variable(context, context.hook_dict)

        # Run the operator
        if context.hook_dict['merge'] if 'merge' in context.hook_dict else False:
            to_merge, post_gen_hook = run_operator(context, mode)
            context.output_dict.update(to_merge)
        else:
            context.output_dict[context.key], post_gen_hook = run_operator(
                context, mode
            )
        if post_gen_hook:
            context.post_gen_hooks.append(post_gen_hook)

        if append_key:
            return context.output_dict[context.key]

    return context.output_dict


def _evaluate_confirm(context: 'Context'):
    if 'confirm' in context.hook_dict:
        if isinstance(context.hook_dict['confirm'], str):
            return prompt(
                [
                    {
                        'type': 'confirm',
                        'name': 'tmp',
                        'message': context.hook_dict['confirm'],
                    }
                ]
            )['tmp']
        elif isinstance(context.hook_dict['confirm'], dict):
            when_condition = True
            if 'when' in context.hook_dict['confirm']:
                when_condition = evaluate_when(
                    self, self.env, self.cc_dict, self.context_key,  # noqa
                )
            if when_condition:
                return prompt(
                    [
                        {
                            'type': 'confirm',
                            'name': 'tmp',
                            'message': context.hook_dict['confirm']['message'],
                            'default': context.hook_dict['confirm']['default'],
                        }
                    ]
                )['tmp']