"""
app starter
"""
from flask import Flask, jsonify, request
import data_management, add_comment

class ClassApp():
    """
    Class app for start the API
    """
    def __init__(self):
        """
        Function init
        """
        self.app = Flask(__name__)
        self.app.config['JSON_SORT_KEYS'] = False
        self.app.config['JSON_AS_ASCII'] = False

        @self.app.route('/target/<string:targetid>/comments', methods =  ["GET"] )
        def __get_target(targetid):
            """
            Function to get all comments linked to one object
            :param targetid: str
            :return: dict
            """
            if data_management.ClassData().check_target_id_existing(targetid) == True:
                #we check that the target_id is a comment
                if targetid[:7] == 'Comment':
                    return jsonify(data_management.ClassData().return_target_comment(targetid))

                else:
                    return jsonify(data_management.ClassData().return_target(targetid))

            else:
                return jsonify({"description": "Comment not found"}), 404

        @self.app.route('/target/<string:targetid>/comments', methods =  ["POST"] )
        def __post_target(targetid):
            """
            Function to add a comment on an object
            :param targetid: str
            :return: dict
            """
            if 'comment' in request.json and len(request.json) == 1:
                comment = request.json['comment']
                add_comment.ClassAddComment().create_comment(comment,targetid)
                return jsonify({"description": "Comment created"})

            else:
                return jsonify({"title": "Request data failed validation","description": "'comment' is the unique mandatory property"}), 404

    def app_starter(self):
        """
        Function to start the API
        :return:
        """
        self.app.run(debug=True)

if __name__ == "__main__":
    ClassApp().app_starter()



