#!/usr/bin/env python3
''' Contains BaseModel class '''
from datetime import datetime
from pydantic import BaseModel as Pydantic
from typing import Optional
from uuid import uuid4

time = '%Y-%m-%dT%H:%M:%S.%f'


class BaseModel(Pydantic):
    ''' The BaseModel class from which future classes will be derived '''

    id: Optional[str] = None
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None
    __collection__: Optional[str] = None

    def __init__(self, **kwargs: dict) -> object:
        ''' Initialization of the base model '''

        for key, val in kwargs.items():
            if key != '__class__' and key != '__collection__':
                self.__setattr__(key, val)
        if kwargs.get('created_at'):
            created_at = datetime.strptime(kwargs['created_at'], time)
            self.__setattr__('created_at', created_at)
        else:
            self.__setattr__('created_at', datetime.utcnow())
        if kwargs.get('updated_at'):
            updated_at = datetime.strptime(kwargs['updated_at'], time)
            self.__setattr__('updated_at', updated_at)
        else:
            self.__setattr__('updated_at', datetime.utcnow())
        if not kwargs.get('id'):
            self.__setattr__('id', str(uuid4()).replace('-', '')[:20])

    def __setattr__(self, name: str, val: str) -> None:
        ''' sets an attribute by ignoring the
        Pydantic AttributeError: __fields_set__ '''
        if name != '__class__' and name != '__collection__':
            object.__setattr__(self, name, val)

    def __str__(self) -> str:
        ''' String representation of the BaseModel class '''
        _dict = self.__dict__.copy()
        if _dict.get('password'):
            _dict['password'] = 'PROTECTED-DATA'

        return f'[{self.__class__.__name__}] ({self.id}) {_dict}'

    def __repr__(self) -> str:
        ''' Representation of the BaseModel class '''
        return self.__str__()

    def to_dict(self, show_passwords: bool = False) -> dict:
        ''' Convert an object to its dict representation '''
        _dict = self.__dict__.copy()
        if 'created_at' in _dict:
            _dict['created_at'] = _dict['created_at'].strftime(time)
        if 'updated_at' in _dict:
            _dict['updated_at'] = _dict['updated_at'].strftime(time)
        _dict['__class__'] = self.__class__.__name__

        if not show_passwords:
            if _dict.get('password'):
                _dict['password'] = 'PROTECTED-DATA'

        return _dict

    def save(self) -> None:
        ''' Updates the attribute 'updated_at' with the current datetime
        and save data '''
        from models import storage
        self.__setattr__('updated_at', datetime.utcnow())
        storage.save(self.__collection__, self.to_dict(show_passwords=True))

    def delete(self) -> None:
        ''' remove the object '''
        storage.delete(self.__collection__, self.id)


if __name__ == "__main__":
    pass
