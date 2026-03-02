from flask_sqlalchemy import SQLAlchemy
from flask_pymongo import PyMongo
from flask_jwt_extended import JWTManager

db = SQLAlchemy()
mongo = PyMongo()
jwt = JWTManager()