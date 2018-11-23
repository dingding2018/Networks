#encoding: utf-8
import os


DEBUG = True

SECRET_KEY = os.urandom(24)

#dialect_driver://username:password@host:port/database
#DIALECT = 'mysql'
#DRIVER = 'pymysql'
HOSTNAME = '127.0.0.1'
PORT = '3306'
DATABASE = 'test_demo'
USERNAME = 'root'
PASSWORD = 'root'

DB_URI = "mysql+pymysql://{}:{}@{}:{}/{}?charset=utf8".format(USERNAME,PASSWORD,HOSTNAME,PORT,DATABASE)
SQLALCHEMY_DATABASE_URI = DB_URI
SQLALCHEMY_TRACK_MODIFICATIONS = False