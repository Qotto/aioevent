#!/usr/bin/env python
# coding: utf-8
# Copyright (c) Qotto, 2019


__all__ = [
    'StoreKeyNotFound',
    'StoreMetadataCantNotUpdated',
    'StorePartitionAlreadyAssigned',
    'StorePartitionNotAssigned',
]


class StoreKeyNotFound(Exception):
    """StoreKeyNotFound

    This error was raised when store not found value by key
    """
    pass


class StoreMetadataCantNotUpdated(Exception):
    """StoreMetadataCantNotUpdated

    This error was raised when store can't update StoreMetadata
    """
    pass


class StorePartitionAlreadyAssigned(Exception):
    """StorePartitionAlreadyAssigned

    This error was raised when store is already assigned on topic
    """
    pass


class StorePartitionNotAssigned(Exception):
    """StorePartitionNotAssigned

    This error was raised when store have not assigned partition
    """
    pass
