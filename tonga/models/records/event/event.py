#!/usr/bin/env python
# coding: utf-8
# Copyright (c) Qotto, 2019

""" BaseEvent module

A *event* is a record to describes what happened in the system.
"""

from typing import Dict, Any

from tonga.models.records.base import BaseRecord


class BaseEvent(BaseRecord):
    """BaseEvent class, all *classic* events must inherit from this class.
    """
    def __init__(self, **kwargs):
        """BaseEvent constructor

        Args:
            **kwargs : see BaseModel class
        """
        super().__init__(**kwargs)

    @classmethod
    def event_name(cls) -> str:
        """ Return BaseEvent name, used in serializer

        Raises:
            NotImplementedError: Abstract def

        Returns:
            None
        """
        raise NotImplementedError

    def to_dict(self) -> Dict[str, Any]:
        """ Serialize BaseRecord to dict

        Raises:
            NotImplementedError: Abstract def

        Returns:
            Dict[str, Any]: class in dict format
        """
        raise NotImplementedError

    @classmethod
    def from_dict(cls, dict_data: Dict[str, Any]):
        """ Deserialize dict to BaseRecord

        Args:
            dict_data (Dict|str, Any]): Contains all BaseRecord Class attribute for return an instanced class

        Raises:
            NotImplementedError: Abstract def

        Returns:
            None
        """
        raise NotImplementedError
