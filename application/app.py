from models import LanguagesSchema, Languages, Dictionaries, DictionariesSchema, Words, WordsSchema, db
from flask import Flask, request, jsonify
from sqlalchemy import or_


URL_PATH = '/api/v1/'

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:@localhost/polyglot'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False


language_schema = LanguagesSchema()
languages_schema = LanguagesSchema(many=True)
dictionary_schema = DictionariesSchema()
dictionaries_schema = DictionariesSchema(many=True)
words_schema = WordsSchema()
words_schema = WordsSchema(many=True)


@app.route('/')
def home():
    return "Welcome"


@app.route(URL_PATH + 'languages', methods=['GET'])
def get_languages():
    languages = Languages.query.all()
    return jsonify(languages_schema.dump(languages))


@app.route(URL_PATH + 'language', methods=['POST'])
def create_language():
    new_language = Languages(
        language=request.json['language'], status=request.json['status'])
    db.session.add(new_language)
    db.session.commit()
    return language_schema.jsonify(new_language)


@app.route(URL_PATH + 'dictionaries', methods=['GET'])
def get_dictionaries():
    languageId = request.args.get('languageId')
    dictionaries = []
    if languageId is None:
        dictionaries = Dictionaries.query.all()
    else:
        dictionaries = Dictionaries.query.filter_by(languageId=languageId)

    return jsonify(dictionaries_schema.dump(dictionaries))


@app.route(URL_PATH + 'dictionary', methods=['POST'])
def create_dictionary():
    new_dictionary = Dictionaries(
        name=request.json['name'], description=request.json['description'], languageId=request.json['languageId'], status=request.json['status'])
    db.session.add(new_dictionary)
    db.session.commit()
    return dictionary_schema.jsonify(new_dictionary)


@app.route(URL_PATH + 'words', methods=['GET'])
def get_words():
    dictionaryId = request.args.get('dictionaryId')
    words = []
    if dictionaryId is None:
        words = Words.query.filter(
            or_(Words.status == 'ACTIVE', Words.status == 'LEARNING')).limit(20)
    else:
        words = Words.query.filter_by(dictionaryId=dictionaryId).filter(
            or_(Words.status == 'ACTIVE', Words.status == 'LEARNING')).limit(20)

    return jsonify(words_schema.dump(words))


@app.route(URL_PATH + 'word', methods=['POST'])
def create_word():
    new_word = Words(
        word=request.json['word'], description=request.json['description'], dictionaryId=request.json['dictionaryId'], status=request.json['status'])
    db.session.add(new_word)
    db.session.commit()
    return dictionary_schema.jsonify(new_word)


@app.route(URL_PATH + 'word/<id>', methods=['PATCH'])
def update_word(id):
    word = Words.query.get(id)
    word.status = request.json['status']
    db.session.commit()
    return dictionary_schema.jsonify(word)


@ app.errorhandler(404)
def page_not_found(error):
    return "Resource not found", 404


if __name__ == '__main__':
    db.init_app(app)
    db.app = app
    db.create_all()
    app.run(debug=True)
