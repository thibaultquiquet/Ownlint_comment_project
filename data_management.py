"""
Database Management
"""
from pymongo import MongoClient
import certifi

class ClassData():
    """
    Class to manage all the Data of the projet
    I decided to chose MongoDB for my data management
    I have created an online account where anyone can manage the data from any IP address.
    I used certifi because MongoClient require TLS certificate for secure communication sometimes
    python is unable request via TLS so here we explicitly mentioning for MongoClient to request
    to mongodb using certifi package
    """
    def __init__(self):
        """
        Function init
        """
        self.cluster = MongoClient(
            "mongodb+srv://thibaultquiquet:6bDohEeKGpj$ynAa@cluster0.vg72q7e.mongodb.net/?retryWrites=true&w=majority",
            tlsCAFile=certifi.where())
        self.db = self.cluster["owlint"]

    def check_target_id_existing(self, target_id):
        """
        Function to ensure that the target_id exists
        I decided that in my database, each collection corresponds to a target
        :param target_id: str
        :return: bool
        """

        for col in self.db.list_collections():
            if col["name"] == target_id:
                return True

        print('ok')
        return False

    def check_comment_id_existing(self, comment_id):
        """
        Function to ensure that the comment_id exists
        :param comment_id: str
        :return: bool
        """
        for col in self.db.list_collections():
            collection = self.db[col["name"]]
            for document in collection.find():
                print(document)
                if comment_id == document['id']:
                    return True
        return False

    def add_comment_in_target(self, target_id, json_target):
        """
        Function to add a new comment in a target

        :param target_id: str
        :param json_target: dict
        :return:
        """

        #we check that the target_id exists
        if json_target['targetId'] != target_id:
            return "Error: You can't add a comment in this collection because you have a wrong target ID"

        collection = self.db[target_id]
        collection.insert_one(json_target)

    def create_new_target(self, target_id):
        """
        This function allows to create a new target_id only in case of first answer to a comment
        :param target_id: str
        :return:
        """
        for col in self.db.list_collections():
            collection = self.db[col["name"]]
            for element in collection.find():
                del element['_id']
                if target_id == element['id']:
                    print(element)
                    collection = self.db[target_id]
                    collection.insert_one(element)

    def return_target(self, target_id):
        """
        Function that allows to properly format the databases of a target
        :param target_id: str
        :return:
        """
        collection = self.db[target_id]
        list_element = []
        for element in collection.find():
            del element['_id']
            list_element.append(element)

        return list_element

    def return_target_comment(self, target_id):
        """
        Function that allows to properly format the databases of a target
        when the target is a comment
        :param target_id:
        :return:
        """
        collection = self.db[target_id]
        list_element = []
        comment_collection = {}
        for element in collection.find():
            del element['_id']
            if target_id == element['id']:
                comment_collection = element
            else:
                list_element.append(element)

        comment_collection['replies'] = list_element
        return comment_collection

print(ClassData().return_target_comment("test_comment"))