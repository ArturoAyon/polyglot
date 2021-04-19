from models import LanguagesSchema, Languages, Dictionaries, DictionariesSchema, Words, WordsSchema, db
from flask import Flask, request, jsonify
from sqlalchemy import or_, event


URL_PATH = '/api/v1/'

app = Flask(__name__)
app.config.from_pyfile('config.cfg')
db.init_app(app)
db.app = app
db.create_all()
db.session.commit()

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
    languageid = request.args.get('languageid')
    dictionaries = []
    if languageid is None:
        dictionaries = Dictionaries.query.all()
    else:
        dictionaries = Dictionaries.query.filter_by(languageId=languageid)

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
    dictionaryid = request.args.get('dictionaryid')
    words = []
    if dictionaryid is None:
        words = Words.query.filter(
            or_(Words.status == 'ACTIVE', Words.status == 'LEARNING')).limit(20)
    else:
        words = Words.query.filter_by(dictionaryId=dictionaryid).filter(
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


# @event.listens_for(Languages.__table__, 'after_create')
# def insert_initial_values_languages(*args, **kwargs):
db.session.add(Languages(language="Spanish", status='ACTIVE'))
db.session.add(Languages(language="Scots", status='ACTIVE'))
db.session.add(Languages(language="Cantonese", status='ACTIVE'))
db.session.add(Languages(language="Chinese (Mandarin)", status='ACTIVE'))
db.session.add(Languages(language="Italian", status='ACTIVE'))
db.session.commit()


# @event.listens_for(Dictionaries.__table__, 'after_create')
# def insert_initial_values_dictionaries(*args, **kwargs):
db.session.add(Dictionaries(name="Useful Spanish phrases", status='ACTIVE',
                            description='A collection of useful phrases in Spanish, a Romance language spoken in Spain and most of South and Central America.', languageId=1))
db.session.add(Dictionaries(name="Family words", status='ACTIVE',
                            description='Words for family members and other relatives in Spanish.', languageId=1))
db.session.add(Dictionaries(name="Useful Scots phrases", status='ACTIVE',
                            description='A collection of useful phrases in Scots, a West Germanic language spoken in Scotland.', languageId=2))
db.session.add(Dictionaries(name="Family words in Scots", status='ACTIVE',
                            description='Words for family members and other relatives in Scots (Scots Leid), a West Germanic language spoken mainly in Scotland and Northern Ireland.', languageId=2))
db.session.add(Dictionaries(name="Family words in Cantonese", status='ACTIVE',
                            description='Words for family members and other relatives in Cantonese, a variety of Chinese spoken in Guangzhou, Hong Kong, Macau and many parts of Southeast Asia.', languageId=3))
db.session.add(Dictionaries(name="Telling the time in Cantonese", status='ACTIVE',
                            description='How to tell the time in Cantonese, a variety of Chinese spoken in southern China and in many overseas Chinese communities.', languageId=3))
db.session.add(Dictionaries(name="Numbers in Mandarin Chinese", status='ACTIVE',
                            description='How to count in Mandarin Chinese, a variety of Chinese spoken in China, Taiwan and various other places.', languageId=4))
db.session.add(Dictionaries(name="Family words in Mandarin", status='ACTIVE',
                            description='Words for family members and other relatives in Mandarin Chinese (Putonghua), a Sinitic language spoken in China, Taiwan and many other places.', languageId=4))
db.session.add(Dictionaries(name="Family words in Italian", status='ACTIVE',
                            description='Words for family members and other relatives in Italian (italiano).', languageId=5))
db.session.add(Dictionaries(name="Colour words in Italian", status='ACTIVE',
                            description='Words for colours in Italian.', languageId=5))
db.session.commit()


# @event.listens_for(Words.__table__, 'after_create')
# def insert_initial_values_languages(*args, **kwargs):
db.session.add(Words(word="Bienvenido",
                     description='Welcome', status='ACTIVE', dictionaryId=1))
db.session.add(Words(word="Hola", description='Hello',
                     status='ACTIVE', dictionaryId=1))
db.session.add(Words(word="¿Cómo estás?",
                     description='How are you?', status='ACTIVE', dictionaryId=1))
db.session.add(Words(word="Padre", description='Father',
                     status='ACTIVE', dictionaryId=2))
db.session.add(Words(word="Madre", description='Mother',
                     status='ACTIVE', dictionaryId=2))
db.session.add(Words(word="Wylcome", description='Welcome',
                     status='ACTIVE', dictionaryId=3))
db.session.add(Words(word="Whit like?",
                     description='How are you?', status='ACTIVE', dictionaryId=3))
db.session.add(Words(word="Mither", description='Mother',
                     status='ACTIVE', dictionaryId=4))
db.session.add(Words(word="Daughter",
                     description='Dochter', status='ACTIVE', dictionaryId=4))
db.session.add(Words(word="父母 (fuhmóuh)",
                     description='Parents', status='ACTIVE', dictionaryId=5))
db.session.add(Words(word="父親 (fuhchàn)",
                     description='Father', status='ACTIVE', dictionaryId=5))
db.session.add(Words(word="而家幾點呀? (yīgā géidím a?)",
                     description='What time is it?', status='ACTIVE', dictionaryId=6))
db.session.add(Words(word="而家中午 (yīgā jungńgh)",
                     description='it is midday', status='ACTIVE', dictionaryId=6))
db.session.add(Words(word="第一 (dìyī)", description='One',
                     status='ACTIVE', dictionaryId=7))
db.session.add(Words(word="第二 (dìèr)", description='Two',
                     status='ACTIVE', dictionaryId=7))
db.session.add(Words(word="老公 (lǎogong)",
                     description='Wusband', status='ACTIVE', dictionaryId=8))
db.session.add(Words(word="老婆 (lǎopó)",
                     description='Wife', status='ACTIVE', dictionaryId=8))
db.session.add(Words(word="Papà", description='Father',
                     status='ACTIVE', dictionaryId=9))
db.session.add(Words(word="Mamma", description='Mother',
                     status='ACTIVE', dictionaryId=9))
db.session.add(Words(word="Nero", description='Black',
                     status='ACTIVE', dictionaryId=10))
db.session.add(Words(word="Bianco", description='White',
                     status='ACTIVE', dictionaryId=10))
db.session.commit()
