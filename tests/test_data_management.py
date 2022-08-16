import unittest
import data_management
from pymongo import MongoClient
import certifi

class ClassTestData(unittest.TestCase):

    def test_check_target_id_existing(self):
        target_id = data_management.ClassData().check_target_id_existing("Photo-bdgetr657434hfggrt8374")
        self.assertEqual(target_id, True)

    def test_check_target_id_is_not_existing(self):
        target_id = data_management.ClassData().check_target_id_existing("Photo-other")
        self.assertEqual(target_id, False)

    def test_check_comment_id_existing(self):
        comment_id = data_management.ClassData().check_comment_id_existing("Comment-huws0k5ml5pnzm2sz3cj0")
        self.assertEqual(comment_id, True)

    def test_check_comment_id_is_not_existing(self):
        comment_id = data_management.ClassData().check_comment_id_existing("Comment-other")
        self.assertEqual(comment_id, False)

    def test_add_comment_in_target(self):
        add_comment = data_management.ClassData().add_comment_in_target("test_collection", {'targetId': 'test_collection'})
        self.assertEqual(add_comment, None)
        cluster = MongoClient(
            "mongodb+srv://thibaultquiquet:6bDohEeKGpj$ynAa@cluster0.vg72q7e.mongodb.net/?retryWrites=true&w=majority",
            tlsCAFile=certifi.where())
        db = cluster["owlint"]
        collection = db["test_collection"]
        collection.delete_many({})

    def test_error_add_comment_in_target(self):
        add_comment = data_management.ClassData().add_comment_in_target("test_bidon", {'targetId': 'test_collection'})
        self.assertEqual(add_comment, "Error: You can't add a comment in this collection because you have a wrong target ID")

    def test_create_new_target(self):
        create_target = data_management.ClassData().create_new_target("test-2")
        self.assertEqual(create_target, None)
        cluster = MongoClient(
            "mongodb+srv://thibaultquiquet:6bDohEeKGpj$ynAa@cluster0.vg72q7e.mongodb.net/?retryWrites=true&w=majority",
            tlsCAFile=certifi.where())
        db = cluster["owlint"]
        collection = db["test-2"]
        collection.drop()

    def test_return_target(self):
        target_return = data_management.ClassData().return_target("test")
        self.assertEqual(target_return,[{'id': 'jkljtfkr'}])

    def test_return_comment(self):
        target_return = data_management.ClassData().return_target_comment("test_comment")
        self.assertEqual(target_return,{'id': 'test_comment', 'replies': [{'id': 'test-2'}]})
