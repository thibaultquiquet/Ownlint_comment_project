"""
Adding and formatting comments
"""
from deep_translator import GoogleTranslator
import data_management
import requests
import string
import random
import time
import json

class ClassAddComment():
    """
    Class to add and format comments
    we take care of translating the comments with the library deep_translator,
    we also create the IDs we need,
    and finally we don't forget to send the comment to the backend service
    """
    def __init__(self):
        self.data = data_management.ClassData()

    def create_comment(self,comment, target_id):
        """
        Function to format the comment as requested in the Swagger documentation
        :param comment: str
        :param target_id: str
        :return:
        """
        comment_id = self.generate_random_id("comment")
        author_id = self.generate_random_id("user")

        #identification of the comment language
        if self.auto_translate(comment)[1] == 'en':
            comment_fr = comment
            comment_en = self.auto_translate(comment)[0]
        else:
            comment_fr = self.auto_translate(comment)[0]
            comment_en = comment

        #timestamp recovery
        ts = str(int(time.time()))

        json_file = {
            "id": comment_id,
            "textFr": comment_fr,
            "textEn": comment_en,
            "publishedAt": ts,
            "authorId":author_id,
            "targetId":target_id
        }

        #Either the target_id exists, in which case we add the comment in the comment thread of this target
        if self.data.check_target_id_existing(target_id) == True :
            self.data.add_comment_in_target(target_id, json_file)
            self.post_message_backend(comment, author_id)

        #Either the target_id does not exist, but the comment to be added is a response to a comment,
        # then we create a new collection in mongoDB and add the comment to it
        elif self.data.check_target_id_existing(target_id) == False and \
                self.data.check_comment_id_existing(target_id) == True:
            self.data.create_new_target(target_id)
            self.data.add_comment_in_target(target_id, json_file)
            self.post_message_backend(comment, author_id)

        else:
            return "Error, the target_id doesn't exist"

    def auto_translate(self,comment):
        """
        Function to translate comments
        we assume that the commentary is in French, and we translate it into English.
        But I say that if the translated comment is equal to the comment in parameter,
        then we must translate it in French
        :param comment: str
        :return:
        """
        language = 'en'
        translated = GoogleTranslator(source='auto', target=language).translate(comment)
        if translated == comment:
            language = 'fr'
            translated = GoogleTranslator(source='auto', target=language).translate(comment)
        return translated, language

    def generate_random_id(self,type_id):
        """
        Function to create ideas for comments or users
        :param type_id: str
        :return:
        """
        characters = list(string.ascii_lowercase + string.digits)
        random.shuffle(characters)
        list_characters = []
        for i in range(21):
            list_characters.append(random.choice(characters))
        random.shuffle(list_characters)

        if type_id == 'comment':
            id = "Comment-" + "".join(list_characters)

        elif type_id == 'user':
            id = "User-" + "".join(list_characters)

        else:
            return "Error: the type must be 'comment' or 'user'"

        #if the comment_id already (which is unlikely to happen), we regenerate a new one
        if self.data.check_comment_id_existing(id) == True:
            self.generate_random_id("comment")

        return id

    def post_message_backend(self, message, author):
        """
        Function to send the message to the backend service
        :param message: str
        :param author: str
        :return:
        """

        json_message = {
            "message": message,
            "author": author
        }

        headers = {
            'Content-Type': 'application/json',
            'user-agent': 'Mozilla/5.0 (X11; U; Linux i686) Gecko/20071127 Firefox/2.0.0.11'
        }

        url = "https://faulty-backend.herokuapp.com/on_comment"
        requests.post(url, data=json.dumps(json_message).encode('utf-8'), headers=headers)
