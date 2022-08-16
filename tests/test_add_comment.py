import add_comment
import unittest
from pymongo import MongoClient
import certifi

class ClassTestAddComment(unittest.TestCase):

    def test_add_comment_when_create_comment_target_id_exist(self):
        create_comment = add_comment.ClassAddComment().create_comment("Bonjour je suis un nouveau test", "test_collection")
        self.assertEqual(create_comment, None )
        cluster = MongoClient(
            "mongodb+srv://thibaultquiquet:6bDohEeKGpj$ynAa@cluster0.vg72q7e.mongodb.net/?retryWrites=true&w=majority",
            tlsCAFile=certifi.where())
        db = cluster["owlint"]
        collection = db["test_collection"]
        collection.delete_many({})

    def test_add_comment_when_create_comment_comment_id_exist(self):
        create_comment = add_comment.ClassAddComment().create_comment("Bonjour", "Comment-huws0k5ml5pnzm2sz3cj0")
        self.assertEqual(create_comment, None )
        cluster = MongoClient(
            "mongodb+srv://thibaultquiquet:6bDohEeKGpj$ynAa@cluster0.vg72q7e.mongodb.net/?retryWrites=true&w=majority",
            tlsCAFile=certifi.where())
        db = cluster["owlint"]
        collection = db["Comment-huws0k5ml5pnzm2sz3cj0"]
        collection.drop()

    def test_add_comment_when_create_comment_target_id_not_exist(self):
        create_comment = add_comment.ClassAddComment().create_comment("Bonjour", "test_target_id")
        self.assertEqual(create_comment, "Error, the target_id doesn't exist" )

    def test_auto_translate_english(self):
        translated_comment = add_comment.ClassAddComment().auto_translate("Hello, I'm a test")
        self.assertEqual(translated_comment, ('Bonjour, je suis un test', 'fr') )

    def test_auto_translate_french(self):
        translated_comment = add_comment.ClassAddComment().auto_translate("Bonjour, je suis un test")
        self.assertEqual(translated_comment,   ('Hello, I am a test', 'en') )

    def test_add_comment_when_generate_random_id_user(self):
        random_id = add_comment.ClassAddComment().generate_random_id("user")
        self.assertEqual(random_id.startswith('User'), True)

    def test_add_comment_when_generate_random_id_comment(self):
        random_id = add_comment.ClassAddComment().generate_random_id("comment")
        self.assertEqual(random_id.startswith('Comment'), True)

    def test_add_comment_when_generate_random_id_other(self):
        random_id = add_comment.ClassAddComment().generate_random_id("other")
        self.assertEqual(random_id, "Error: the type must be 'comment' or 'user'")

    def test_post_message_backend(self):
        message_post = add_comment.ClassAddComment().post_message_backend("test","unknow")
        self.assertEqual(message_post, None)
