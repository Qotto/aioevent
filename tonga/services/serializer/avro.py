#!/usr/bin/env python
# coding: utf-8
# Copyright (c) Qotto, 2019

import json
import os
import re
from io import BytesIO
from logging import Logger, getLogger
from typing import Dict, Any, Union, Type

from avro.datafile import DataFileWriter, DataFileReader
from avro.io import DatumWriter, DatumReader, AvroTypeException
from avro.schema import NamedSchema, Parse
from yaml import FullLoader, load_all  # type: ignore

from tonga.models.events.base import BaseModel
from tonga.models.handlers.base import BaseHandler
from tonga.models.store_record.base import BaseStoreRecordHandler, BaseStoreRecord
from tonga.services.serializer.errors import (AvroEncodeError, AvroDecodeError, AvroAlreadyRegister,
                                              NotMatchedName, MissingEventClass, MissingHandlerClass)
from .base import BaseSerializer

__all__ = [
    'AvroSerializer',
]


class AvroSerializer(BaseSerializer):
    """Class serializer Avro schema to class instance

    Attributes:
        AVRO_SCHEMA_FILE_EXTENSION (str): Constant for Avro schema file extension (default : *avsc.yaml*)
        logger (Logger): Serializer logger
        schemas_folder (Dict[str, NamedSchema]): Dict store all Avro schema after loading in schemas_folder
        _events (Dict[object, Union[Type[BaseModel], Type[BaseStoreRecord]]]): Dict where are stored BaseModel /
                                                                               BaseStoreRecord class
        _handlers (Dict[object, Union[BaseHandler, BaseStoreRecordHandler]]): Dict where are stored BaseHandler /
                                                                               BaseStoreRecordHandler class
    """
    AVRO_SCHEMA_FILE_EXTENSION: str = 'avsc.yaml'
    logger: Logger
    schemas_folder: str
    _schemas: Dict[str, NamedSchema]
    _events: Dict[object, Union[Type[BaseModel], Type[BaseStoreRecord]]]
    _handlers: Dict[object, Union[BaseHandler, BaseStoreRecordHandler]]

    def __init__(self, schemas_folder: str):
        """ AvroSerializer constructor

        Args:
            schemas_folder (str): Folder where are stored project avro schema
                                  (example: *os.path.join(os.path.dirname(os.path.abspath(__file__)),
                                  'examples/coffee_bar/avro_schemas')*)

        Returns:
            None
        """
        super().__init__()
        self.schemas_folder = schemas_folder
        # TODO Remove workaround
        self.schemas_folder_lib = os.path.dirname(os.path.abspath(__file__)) + '/../../models/store_record/avro_schema'
        self.logger = getLogger('tonga')
        self._schemas = dict()
        self._events = dict()
        self._handlers = dict()
        self._scan_schema_folder(self.schemas_folder)
        self._scan_schema_folder(self.schemas_folder_lib)

    def _scan_schema_folder(self, schemas_folder: str) -> None:
        """ AvroSerializer internal function, he was call by class constructor

        Args:
            schemas_folder (str): Folder where are stored project avro schema

        Returns:
            None
        """
        with os.scandir(schemas_folder) as files:
            for file in files:
                if not file.is_file():
                    continue
                if file.name.startswith('.'):
                    continue
                if not file.name.endswith(f'.{self.AVRO_SCHEMA_FILE_EXTENSION}'):
                    continue
                self._load_schema_from_file(file.path)

    def _load_schema_from_file(self, file_path: str) -> None:
        """ AvroSerializer internal function, he was call by _scan_schema_folder for load schema file

        Args:
            file_path: Path to schema

        Raises:
            AvroAlreadyRegister: This error was raised when schema is already register the Avro schema

        Returns:
            None
        """
        with open(file_path, 'r') as fd:
            for s in load_all(fd, Loader=FullLoader):
                avro_schema_data = json.dumps(s)
                avro_schema = Parse(avro_schema_data)
                schema_name = avro_schema.namespace + '.' + avro_schema.name
                if schema_name in self._schemas:
                    raise AvroAlreadyRegister
                self._schemas[schema_name] = avro_schema

    def register_event_handler_store_record(self, store_record_event: Type[BaseStoreRecord],
                                            store_record_handler: BaseStoreRecordHandler) -> None:
        """ Register project event & handler in AvroSerializer

        Args:
            store_record_event (Type[BaseStoreRecord]): Store record event, BaseStoreRecord can work without class
                                                        override, but for more flexibility you can create your own class
            store_record_handler (BaseStoreRecordHandler): Store record handler, can be used with Tonga
                                                           StoreRecordHandler this class work for simple usage, for more
                                                           flexibility creates your own class must inherit form
                                                           BaseStoreRecordHandler

        Examples:
            This is an example with Tonga StoreRecordHandler

            .. code-block:: python

                # Import serializer
                from tonga.services.serializer.avro import AvroSerializer

                # Import store builder
                from tonga.stores.store_builder.store_builder import StoreBuilder

                # Import StoreRecord & StoreRecordHandler
                from tonga.models.store_record.store_record import StoreRecord
                from tonga.models.store_record.store_record_handler import StoreRecordHandler

                serializer = AvroSerializer(os.path.join(os.path.dirname(os.path.abspath(__file__)),
                                            'examples/coffee_bar/avro_schemas'))

                store_builder = StoreBuilder('Some stuff')

                store_record_handler = StoreRecordHandler(store_builder)

                serializer.register_event_handler_store_record(StoreRecord, store_record_handler)

        Returns:
            None
        """
        event_name_regex = re.compile(store_record_event.event_name())
        self._events[event_name_regex] = store_record_event
        self._handlers[event_name_regex] = store_record_handler

    def register_class(self, event_name: str, event_class: Type[BaseModel], handler_class: BaseHandler) -> None:
        """Register project event & handler in AvroSerializer

        Args:
            event_name (str): Event name, Avro schema *namespace + name*
            event_class (Type[BaseModel]): Event class must inherit form *BaseEvent / BaseCommand / BaseResult*
            handler_class (BaseHandler): Handler class must inherit form *BaseHandlerEvent / BaseHandlerCommand
                                        / BaseHandlerResult*

        Raises:
            NotMatchedName: Can’t find same name in registered schema

        Examples:
            .. code-block:: python

                # Import serializer
                from tonga.services.serializer.avro import AvroSerializer

                # Import store builder
                from tonga.stores.store_builder.store_builder import StoreBuilder

                # Import KafkaProducer
                from tonga.services.producer.kafka_producer import KafkaProducer

                # Import waiter events
                from examples.coffee_bar.waiter.models.events.coffee_finished import CoffeeFinished

                # Import waiter handlers
                from examples.coffee_bar.waiter.models.handlers.coffee_finished_handler import CoffeeFinishedHandler

                serializer = AvroSerializer(os.path.join(os.path.dirname(os.path.abspath(__file__)),
                                            'examples/coffee_bar/avro_schemas'))

                store_builder = StoreBuilder('Go to StoreBuilder documentation')
                transactional_producer = KafkaProducer('Go to KafkaProducer documentation')

                coffee_finished_handler = CoffeeFinishedHandler(store_builder, transactional_producer)

                serializer.register_class('tonga.waiter.event.CoffeeFinished', CoffeeFinished, coffee_finished_handler)

        Returns:
            None
        """
        event_name_regex = re.compile(event_name)

        matched: bool = False
        for schema_name in self._schemas:
            if event_name_regex.match(schema_name):
                matched = True
                break
        if not matched:
            raise NotMatchedName
        self._events[event_name_regex] = event_class
        self._handlers[event_name_regex] = handler_class

    def get_schemas(self) -> Dict[str, NamedSchema]:
        """ Return _schemas class attributes

        Returns:
            Dict[str, NamedSchema]: _schemas class attributes
        """
        return self._schemas

    def get_events(self) -> Dict[object, Union[Type[BaseModel], Type[BaseStoreRecord]]]:
        """ Return _events class attributes

        Returns:
            Dict[object, Union[Type[BaseModel], Type[BaseStoreRecord]]]: _events class attributes
        """
        return self._events

    def get_handlers(self) -> Dict[object, Union[BaseHandler, BaseStoreRecordHandler]]:
        """ Return _handlers class attributes

        Returns:
            Dict[object, Union[BaseHandler, BaseStoreRecordHandler]]: _handlers class attributes
        """
        return self._handlers

    def encode(self, obj: BaseModel) -> bytes:
        """ Encode *BaseHandlerEvent / BaseHandlerCommand / BaseHandlerResult* to bytes format

        This function is used by kafka-python

        Args:
            obj (BaseModel): *BaseHandlerEvent / BaseHandlerCommand / BaseHandlerResult*

        Raises:
            MissingEventClass: can’t find BaseModel in own registered BaseModel list (self._schema)
            AvroEncodeError: fail to encode BaseModel to bytes

        Returns:
            bytes: BaseModel in bytes
        """
        try:
            schema = self._schemas[obj.event_name()]
        except KeyError as err:
            self.logger.exception('%s', err.__str__())
            raise MissingEventClass

        try:
            output = BytesIO()
            writer = DataFileWriter(output, DatumWriter(), schema)
            writer.append(obj.__dict__)
            writer.flush()
            encoded_event = output.getvalue()
            writer.close()
        except AvroTypeException as err:
            self.logger.exception('%s', err.__str__())
            raise AvroEncodeError
        return encoded_event

    def decode(self, encoded_obj: Any) -> Dict[str, Union[BaseModel, BaseStoreRecord,
                                                          BaseHandler, BaseStoreRecordHandler]]:
        """ Decode bytes format to BaseModel and return dict which contains decoded *BaseModel / BaseStoreRecord*

        This function is used by kafka-python / internal call

        Args:
            encoded_obj (Any): Bytes encode BaseModel / BaseStoreRecord

        Raises:
            AvroDecodeError: fail to decode bytes in BaseModel
            MissingEventClass: can’t find BaseModel in own registered BaseModel list (self._schema)
            MissingHandlerClass: can’t find BaseHandlerModel in own registered BaseHandlerModel list (self._handler)

        Returns:
            Dict[str, Union[BaseModel, BaseStoreRecord, BaseHandler, BaseStoreRecordHandler]]:
                                                                    example: {'event_class': ..., 'handler_class': ...}
        """
        try:
            reader = DataFileReader(BytesIO(encoded_obj), DatumReader())
            schema = json.loads(reader.meta.get('avro.schema').decode('utf-8'))
            schema_name = schema['namespace'] + '.' + schema['name']
            event_data = next(reader)
        except AvroTypeException as err:
            self.logger.exception('%s', err.__str__())
            raise AvroDecodeError

        # Finds a matching event name
        for e_name, event in self._events.items():
            if e_name.match(schema_name):  # type: ignore
                event_class = event
                break
        else:
            raise MissingEventClass

        # Finds a matching handler name
        for e_name, handler in self._handlers.items():
            if e_name.match(schema_name):  # type: ignore
                handler_class = handler
                break
        else:
            raise MissingHandlerClass
        return {'event_class': event_class.from_data(event_data=event_data), 'handler_class': handler_class}
