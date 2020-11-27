"""Utilities mainly used in helping `modes` like replay and others."""
import json
import oyaml as yaml
import os

from cookiecutter.utils.paths import make_sure_path_exists

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from cookiecutter.models import Settings


def get_file_name(replay_dir, template_name, suffix='yaml'):
    """Get the name of file."""
    suffix = '.' + suffix if not template_name.endswith('.' + suffix) else ''
    file_name = '{}{}'.format(template_name, suffix)
    return os.path.join(replay_dir, file_name)


def dump(output_dir, output_name, output_dict, s: 'Settings'):
    """Write json data to file."""
    if not make_sure_path_exists(output_dir):
        raise IOError('Unable to create replay dir at {}'.format(output_dir))

    replay_file = get_file_name(output_dir, output_name, s.dump_output)

    if s.dump_output == 'json':
        with open(replay_file, 'w') as f:
            json.dump(output_dict, f, indent=2)
    if s.dump_output in ['yaml', 'yml']:
        with open(replay_file, 'w') as f:
            yaml.dump(output_dict, f, indent=2)


def load(replay_dir, template_name, context_key):
    """Read json data from file."""
    if not isinstance(template_name, str):
        raise TypeError('Template name is required to be of type str')

    replay_file = get_file_name(replay_dir, template_name)

    with open(replay_file, 'r') as infile:
        context = json.load(infile)

    if context_key not in context:
        raise ValueError('Context does not contain the context_key %s' % context_key)

    return context
