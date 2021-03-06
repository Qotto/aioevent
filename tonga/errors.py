#!/usr/bin/env python
# coding: utf-8
# Copyright (c) Qotto, 2019

""" Regular packages

Import all tonga exceptions
"""

# Import StoreRecord exceptions
from tonga.models.store.errors import UnknownStoreRecordType

# Import BaseCommand exceptions
from tonga.models.records.command.errors import CommandEventMissingProcessGuarantee

# Import KeyPartitioner & StatefulsetPartitioner exceptions
from tonga.services.coordinator.partitioner.errors import (BadKeyType, OutsideInstanceNumber)

# Import StatefulsetAssignors exceptions
from tonga.services.coordinator.assignors.errors import BadAssignorPolicy

# Import Producer exceptions
from tonga.services.producer.errors import (ProducerConnectionError, AioKafkaProducerBadParams, KafkaProducerError,
                                            KafkaProducerNotStartedError, KafkaProducerAlreadyStartedError,
                                            KafkaProducerTimeoutError, KeyErrorSendEvent, ValueErrorSendEvent,
                                            TypeErrorSendEvent, FailToSendEvent, UnknownEventBase, FailToSendBatch)

# Import Consumer exceptions
from tonga.services.consumer.errors import (ConsumerConnectionError, AioKafkaConsumerBadParams, KafkaConsumerError,
                                            KafkaConsumerNotStartedError, KafkaConsumerAlreadyStartedError,
                                            ConsumerKafkaTimeoutError, IllegalOperation, TopicPartitionError,
                                            NoPartitionAssigned, OffsetError, UnknownHandler,
                                            UnknownStoreRecordHandler, UnknownHandlerReturn, HandlerException)

# Import AvroSerializer & KeySerializer exceptions
from tonga.services.serializer.errors import (AvroAlreadyRegister, AvroEncodeError, AvroDecodeError, NotMatchedName,
                                              MissingEventClass, MissingHandlerClass, KeySerializerDecodeError,
                                              KeySerializerEncodeError)

# Import LocalStore & GlobalStore exceptions
from tonga.stores.errors import (StoreKeyNotFound, StorePartitionAlreadyAssigned, StorePartitionNotAssigned)

# Import StoreBuilder exceptions
from tonga.stores.manager.errors import (UninitializedStore, CanNotInitializeStore, FailToSendStoreRecord)

# Import KafkaClient exceptions
from tonga.services.coordinator.client.errors import (BadArgumentKafkaClient, KafkaClientConnectionErrors,
                                                      KafkaAdminConfigurationError, CurrentInstanceOutOfRange)

__all__ = [
    # StoreRecord exceptions
    'UnknownStoreRecordType',
    # BaseCommand exceptions
    'CommandEventMissingProcessGuarantee',
    # KeyPartitioner & StatefulsetPartitioner exceptions
    'BadKeyType',
    'OutsideInstanceNumber',
    # StatefulsetAssignors exceptions
    'BadAssignorPolicy',
    # Producer exceptions
    'ProducerConnectionError',
    'AioKafkaProducerBadParams',
    'KafkaProducerError',
    'KafkaProducerNotStartedError',
    'KafkaProducerAlreadyStartedError',
    'KafkaProducerTimeoutError',
    'KeyErrorSendEvent',
    'ValueErrorSendEvent',
    'TypeErrorSendEvent',
    'FailToSendEvent',
    'UnknownEventBase',
    'FailToSendBatch',
    # Consumer exceptions
    'ConsumerConnectionError',
    'AioKafkaConsumerBadParams',
    'KafkaConsumerError',
    'KafkaConsumerNotStartedError',
    'KafkaConsumerAlreadyStartedError',
    'ConsumerKafkaTimeoutError',
    'IllegalOperation',
    'TopicPartitionError',
    'NoPartitionAssigned',
    'OffsetError',
    'UnknownHandler',
    'UnknownStoreRecordHandler',
    'UnknownHandlerReturn',
    'HandlerException',
    # AvroSerializer & KeySerializer exceptions
    'AvroAlreadyRegister',
    'AvroEncodeError',
    'AvroDecodeError',
    'NotMatchedName',
    'MissingEventClass',
    'MissingHandlerClass',
    'KeySerializerDecodeError',
    'KeySerializerEncodeError',
    # LocalStore & GlobalStore exceptions
    'StoreKeyNotFound',
    'StorePartitionAlreadyAssigned',
    'StorePartitionNotAssigned',
    # StoreBuilder exceptions
    'UninitializedStore',
    'CanNotInitializeStore',
    'FailToSendStoreRecord',
    # KafkaClient exceptions
    'BadArgumentKafkaClient',
    'CurrentInstanceOutOfRange',
    'KafkaAdminConfigurationError',
    'KafkaClientConnectionErrors'
]
