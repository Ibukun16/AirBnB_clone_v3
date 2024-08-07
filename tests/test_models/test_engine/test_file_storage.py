#!/usr/bin/python3
"""
Contains the TestFileStorageDocs classes
"""

from datetime import datetime
import inspect
import models
from models.engine import file_storage
from models.amenity import Amenity
from models.base_model import BaseModel
from models.city import City
from models.place import Place
from models.review import Review
from models.state import State
from models.user import User
import json
import os
import pep8
import unittest
FileStorage = file_storage.FileStorage
classes = {"Amenity": Amenity, "BaseModel": BaseModel, "City": City,
           "Place": Place, "Review": Review, "State": State, "User": User}


class TestFileStorageDocs(unittest.TestCase):
    """Tests to check the documentation and style of FileStorage class"""
    @classmethod
    def setUpClass(cls):
        """Set up for the doc tests"""
        cls.fs_f = inspect.getmembers(FileStorage, inspect.isfunction)

    def test_pep8_conformance_file_storage(self):
        """Test that models/engine/file_storage.py conforms to PEP8."""
        pep8s = pep8.StyleGuide(quiet=True)
        result = pep8s.check_files(['models/engine/file_storage.py'])
        self.assertEqual(result.total_errors, 0,
                         "Found code style errors (and warnings).")

    def test_pep8_conformance_test_file_storage(self):
        """Test tests/test_models/test_file_storage.py conforms to PEP8."""
        pep8s = pep8.StyleGuide(quiet=True)
        result = pep8s.check_files(['tests/test_models/test_engine/\
test_file_storage.py'])
        self.assertEqual(result.total_errors, 0,
                         "Found code style errors (and warnings).")

    def test_file_storage_module_docstring(self):
        """Test for the file_storage.py module docstring"""
        self.assertIsNot(file_storage.__doc__, None,
                         "file_storage.py needs a docstring")
        self.assertTrue(len(file_storage.__doc__) >= 1,
                        "file_storage.py needs a docstring")

    def test_file_storage_class_docstring(self):
        """Test for the FileStorage class docstring"""
        self.assertIsNot(FileStorage.__doc__, None,
                         "FileStorage class needs a docstring")
        self.assertTrue(len(FileStorage.__doc__) >= 1,
                        "FileStorage class needs a docstring")

    def test_fs_func_docstrings(self):
        """Test for the presence of docstrings in FileStorage methods"""
        for func in self.fs_f:
            self.assertIsNot(func[1].__doc__, None,
                             "{:s} method needs a docstring".format(func[0]))
            self.assertTrue(len(func[1].__doc__) >= 1,
                            "{:s} method needs a docstring".format(func[0]))


@unittest.skipIf(models.storage_t == 'db', "not testing file storage")
class TestFileStorage(unittest.TestCase):
    """Test the FileStorage class"""
    def test_all_returns_dict(self):
        """Test that all returns the FileStorage.__objects attr"""
        storage = FileStorage()
        new_dict = storage.all()
        self.assertEqual(type(new_dict), dict)
        self.assertIs(new_dict, storage._FileStorage__objects)

    def test_new(self):
        """test that new adds an object to the FileStorage.__objects attr"""
        state_data = {"name": "Lagos"}
        new_state = State(**state_data)

        models.storage.new(new_state)

        session = models.storage._FileStorage__session

        retrieveed_state = session.query(State).filter_by(id=new_state).first()

        self.asserEqual(retrieved_state.id, new_state.id)
        self.assertEqual(retrieved_state.name, new_state.name)
        self.assertIsNotNone(retrieved_state)

    def test_save(self):
        """Test that save properly saves objects to file.json"""
        state_data = {"name": "Ogun"}
        new_state = State(**state_data)

        models.storage.new(new_state)

        models.storage.save()

        session = models.storage._FileStorage__session

        retrieved_state = session.quuery(State).filter_by(id=new_state).first()

        self.asserEqual(retrieved_state.id, new_state.id)
        self.assertEqual(retrieved_state.name, new_state.name)
        self.assertIsNotNone(retrieved_state)

    def test_get(self):
        """Test that get returns an object based on a given class and id."""
        storage = FileStorage()

        storage.reload()

        state_data = {"name": "California"}

        state_instance = State(**state_data)
        storage.new(state_instance)
        storage.save()

        retrieved_state = storage.get(State, state_instance.id)

        self.assertEqual(state_instance, retrieved_state)

        fake_state_id = storage.get(State, 'fake_id')

        self.assertEqual(fake_state_id, None)

    def test_count(self):
        """Test that count the number of objects based on a given class"""
        storage = FileStorage()
        storage.reload()
        state_data = {"name": "Lagos"}
        state_instance = State(**state_data)
        storage.new(state_instance)

        city_data = {"name": "Alimosho", "state_id": state_instance.id}

        city_instance = City(**city_data)

        storage.new(city_instance)

        storage.save()

        state_occurrence = storage.count(State)
        self.assertEqual(state_occurrence, len(storage.all(State)))

        all_occurrence = storage.count()
        self.assertEqual(state_occurrence, len(storage.all()))
