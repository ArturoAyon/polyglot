from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from sqlalchemy import Column, ForeignKey, Enum, Integer, String
from sqlalchemy.orm import relationship

db = SQLAlchemy()
ma = Marshmallow()


class Languages(db.Model):
    __tablename__ = 'languages'
    id = Column(db.Integer, primary_key=True)
    language = Column(db.String(100), nullable=False, unique=True)
    status = Column(db.Enum("ACTIVE", "INACTIVE"), default="ACTIVE")
    dictionaries = relationship(
        "Dictionaries", backref="Languages", lazy='dynamic')


class LanguagesSchema(ma.Schema):
    class Meta:
        fields = ('id', 'language', 'status')


class Dictionaries(db.Model):
    __tablename__ = 'dictionaries'
    id = Column(db.Integer, primary_key=True)
    name = Column(db.String(100), nullable=False, unique=True)
    description = Column(db.String(255), nullable=False)
    status = Column(db.Enum("ACTIVE", "INACTIVE"), default="ACTIVE")
    languageId = Column(db.Integer, ForeignKey('languages.id'), nullable=False)
    words = relationship(
        "Words", backref="Dictionaries", lazy='dynamic')


class DictionariesSchema(ma.Schema):
    class Meta:
        fields = ('id', 'name', 'description', 'languageId',
                  'status')


class Words(db.Model):
    __tablename__ = 'words'
    id = Column(db.Integer, primary_key=True)
    word = Column(db.String(50), nullable=False)
    description = Column(db.String(50), nullable=False)
    status = Column(Enum("ACTIVE", "INACTIVE", "LEARNING",
                         "LEARNED"), default="ACTIVE")
    dictionaryId = Column(db.Integer, ForeignKey(
        'dictionaries.id'), nullable=False)


class WordsSchema(ma.Schema):
    class Meta:
        fields = ('id', 'word', 'description', 'status', 'dictionaryId',
                  'languageId',  'status')
