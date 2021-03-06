#!/usr/bin/env python
# coding: utf-8
# Copyright (c) Qotto, 2019

""" BaseCommandHandler Module

All command handler must be inherit from this class. Execute function was called by consumer on each received command.

For make an transaction in execute function return 'transaction' as string after end transaction otherwise return none.
"""

from typing import Union

from tonga.models.handlers.base import BaseHandler
from tonga.models.records.command.command import BaseCommand


__all__ = [
    'BaseCommandHandler'
]


class BaseCommandHandler(BaseHandler):
    """ Base of all command handler
    """

    @classmethod
    def handler_name(cls) -> str:
        """ Return handler name, used by serializer

        Raises:
            NotImplementedError: Abstract def

        Returns:
            None
        """
        raise NotImplementedError

    async def execute(self, event: BaseCommand) -> Union[str, None]:
        """ This function is automatically call by Tonga when an command with same name was receive by consumer

        Args:
            event (BaseCommand): Command event receive by consumer

        Notes:
            If execute make an transaction return 'transaction' as string at transaction end

        Raises:
            NotImplementedError: Abstract def

        Returns:
            None
        """
        raise NotImplementedError
