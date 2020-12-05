#!/usr/bin/env python3
''' User model '''
from models.base_model import BaseModel
from models.engine.authentication import hash_pwd
import re

pwd_re = '^(?=.*?[A-Z])(?=.*?[a-z])(?=.*?[0-9])(?=.*?[#?!@$%^&*-]).{8,}$'

# url_re = r'(http(s)?:\/\/.)?(www\.)?[-a-zA-Z0-9@:%._\+~#=]{2,256}\.[a-z]{2,6}\b([-a-zA-Z0-9@:%_\+.~#?&//=]*)'


class User(BaseModel):
    ''' Gets and handles a user object '''
    __collection__: str = 'Users'

    def __init__(self, **kwargs) -> object:
        ''' instantiate the object '''
        password = kwargs.get('password')
        if not password:
            raise ValueError('The password cannot be null')

        if type(password) != bytes:  # password not encrypted
            if not re.search(pwd_re, password):
                raise ValueError(
                    'The password must be have minimum eight characters, at ' +
                    'least one uppercase letter, one lowercase letter, one ' +
                    'number and one special character')

            self.__setattr__('password', hash_pwd(password))
            kwargs.pop('password', None)

        self.profile_pic = 'https://picsum.photos/32'

        super().__init__(**kwargs)
