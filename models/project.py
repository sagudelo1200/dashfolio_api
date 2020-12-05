#!/usr/bin/env python3
''' Project model '''
from models.base_model import BaseModel


class Project(BaseModel):
    ''' Gets and handles a project object '''
    __collection__: str = 'Projects'

    def __init__(self, **kwargs: dict) -> object:
        ''' instantiate the object '''
        super().__init__(**kwargs)
