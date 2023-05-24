from flask import Blueprint, request, jsonify, render_template
from helpers import token_required
from models import db, User, Word, word_schema, words_schema

api = Blueprint('api',__name__, url_prefix='/api')

@api.route('/getdata')
def getdata():
    return {'hi': 'there'}


#Create Word Endpoint
@api.route('/words', methods = ['POST'])
@token_required
def create_word(current_user_token):
    saved_word = request.json['saved_word']
    meaning = request.json['meaning']
    word_type = request.json['word_type']
    origin = request.json['origin']
    user_token = current_user_token.token

    print(f'BIG TESTER: {current_user_token.token}')

    word = Word(saved_word, meaning, word_type, origin, user_token = user_token )

    db.session.add(word)
    db.session.commit()

    response = word_schema.dump(word)
    return jsonify(response)

#Retrieve Word Endpoint
@api.route('/words', methods = ['GET'])
@token_required
def get_word(current_user_token):
    a_user = current_user_token.token
    words = Word.query.filter_by(user_token = a_user).all()
    response = words_schema.dump(words)
    return jsonify(response)

#Retrieve One Word Endpoint
@api.route('/words/<id>', methods = ['GET'])
@token_required
def get_word_two(current_user_token, id):
    fan = current_user_token.token
    if fan == current_user_token.token:
        word = Word.query.get(id)
        response = word_schema.dump(word)
        return jsonify(response)
    else:
        return jsonify({"message": "Valid Token Required"}),401

# UPDATE endpoint
@api.route('/words/<id>', methods = ['POST','PUT'])
@token_required
def update_word(current_user_token,id):
    word = Word.query.get(id) 
    word.saved_word = request.json['saved_word']
    word.meaning = request.json['meaning']
    word.word_type = request.json['word_type']
    word.origin = request.json['origin']
    word.user_token = current_user_token.token

    db.session.commit()
    response = word_schema.dump(word)
    return jsonify(response)


# DELETE word ENDPOINT
@api.route('/words/<id>', methods = ['DELETE'])
@token_required
def delete_word(current_user_token,id):
    word = Word.query.get(id)
    db.session.delete(word)
    db.session.commit()
    response = word_schema.dump(word)
    return jsonify(response)