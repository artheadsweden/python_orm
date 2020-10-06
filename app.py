import json

from config import *
from flask import request

from models.user import User, EmailAddress


@app.route('/users', methods=['POST'])
def post_user():
    # get json data
    data_json = request.data
    # create dict from json
    data = json.loads(data_json)
    # create user object
    user = User(username=data['username'])
    # create EmailAdress object for each address
    for item in data["email_addresses"]:
        address = EmailAddress(email=item['email'])
        # append the address to the users email address collection
        user.email_addresses.append(address)

    # add the user to the db session
    db.session.add(user)
    # and commit
    db.session.commit()
    return json.dumps(user.to_dict()), 201

@app.route('/users/<id>/addresses', methods=['POST'])
def post_address(id):
    user = User.query.filter_by(id=id).first()
    if user is None:
        return f"The user with id {id} does not exist", 400

    # get json data
    data_json = request.data
    # create dict from json
    data = json.loads(data_json)
    for item in data['email_addresses']:
        address = EmailAddress(email=item['email'])
        # append the address to the users email address collection
        user.email_addresses.append(address)
    db.session.commit()
    return json.dumps(user.to_dict()), 201

@app.route('/users', methods=['GET'])
def get_users():
    users = User.query.all()
    result = [user.to_dict() for user in users]
    return json.dumps(result), 200

@app.route('/users/<id>', methods=['GET'])
def get_user(id):
    user = User.query.filter_by(id=id).first()
    if user is None:
        return f"The user with id {id} does not exist", 400

    return json.dumps(user.to_dict()), 200

if __name__ == '__main__':
    app.run()
