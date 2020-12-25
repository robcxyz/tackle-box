# -*- coding: utf-8 -*-

"""Block hook."""
from __future__ import unicode_literals
from __future__ import print_function

import logging
from typing import Dict

from tackle.models import BaseHook
import tackle as cc

logger = logging.getLogger(__name__)


class BlockHook(BaseHook):
    """
    Hook  for blocks of hooks.

    This is a special case where the hooks input variables are not rendered
    until it is later executed.

    :param items: Map of inputs
    """

    type: str = 'block'
    items: Dict

    def execute(self):
        return cc.prompt.prompt_for_config(
            context={self.context_key: self.items},
            no_input=self.no_input,
            context_key=self.context_key,
            existing_context=self.cc_dict,
        )