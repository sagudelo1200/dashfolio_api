#!/usr/bin/env python3
''' Firebase storage engine '''
import firebase_admin
from firebase_admin import credentials, firestore
from os import environ
from models.project import Project
from models.user import User
import json

collections = {'Projects': Project, 'Users': User}


class FirebaseStorage:
    ''' performs queries and executes actions on the database '''
    __engine = None
    __db = None

    def __init__(self) -> None:
        ''' Validates the firebase sdk credentials and start de client '''
        CREDENTIALS = environ.get('DASHFOLIO_DB_CREDENTIALS')
        if not CREDENTIALS:
            print('DASHFOLIO_DB_CREDENTIALS was not found')
            CREDENTIALS = input('DASHFOLIO_DB_CREDENTIALS = ')

        try:
            app = credentials.Certificate(CREDENTIALS)
            self.__engine = firebase_admin.initialize_app(app)
            self.__db = firestore.client()
        except FileNotFoundError as e:
            raise FileNotFoundError(f'DASHFOLIO_DB_CREDENTIALS: {e}')
        except json.decoder.JSONDecodeError or ValueError as e:
            raise ValueError('DASHFOLIO_DB_CREDENTIALS: Invalid credentials.')

    def all(self, col: str = None, show_passwords: bool = False) -> dict:
        '''
        query on te current firestorage session and get all docs
        in the indicated collection or in all collections
        '''
        if col and col not in collections:
            return None

        data = {}

        for key, val in collections.items():
            if not col or col == key:
                docs = self.__db.collection(key).stream()
                for doc in docs:
                    obj = doc.to_dict()
                    doc_key = f'{val.__name__}.{doc.id}'
                    obj['__class__'] = val.__name__

                    if obj.get('_class_'):
                        obj.pop('_class_')

                    if not show_passwords:
                        if obj.get('password'):
                            obj['password'] = 'PROTECTED-DATA'

                    obj['id'] = doc.id
                    data[doc_key] = obj
        return data

    def get(self, col: str, id: str) -> object:
        ''' Get the document with the id in the stored collection '''
        if col not in collections:
            return None

        if self.exists(col, id):
            obj = self.__db.collection(col).document(id).get()

            doc = obj.to_dict()
            doc['id'] = id
            if doc.get('_class_'):
                del doc['_class_']
            return collections[col](**doc)
        return None

    def save(self, col: str, doc: dict, replace: bool = False) -> bool:
        ''' save the document in the collection '''
        merge = False
        id = doc.get('id')
        if not id:
            return False

        if self.exists(col, id) and not replace:
            merge = True
            obj = self.get(col, id).to_dict()
            doc['created_at'] = obj.get('created_at') or doc.get('created_at')

        doc_ref = self.__db.collection(col).document(id)

        if doc.get('__class__'):
            doc['_class_'] = doc.get('__class__')
            doc.pop('__class__')

        doc_ref.set(doc, merge=merge)
        return True

    def exists(self, col: str, id: str) -> bool:
        ''' Verifies the existence of a document '''
        if col not in collections:
            return None

        doc = self.__db.collection(col).document(id).get()

        return True if doc.to_dict() else False

    def delete(self, col: str, id: str) -> None:
        ''' delete a document '''
        if col in collections:
            self.__db.collection(col).document(id).delete()

    def count(self, col: str = None) -> int:
        '''count documents in collections '''
        if col and col not in collections:
            return None

        total = 0

        for key, val in collections.items():
            if not col or col == key:
                docs = self.__db.collection(key).select('').get()
                total += len(docs)

        return total
