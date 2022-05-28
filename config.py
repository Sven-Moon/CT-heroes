import os
basedir = os.path.abspath(os.path.dirname(__name__))

# def sqlDBFixer():
#     uri = os.environ.get('SQLALCHEMY_DATABASE_URI')
#     if uri[:8] == 'postgres' and uri[8:10] != 'ql':
#         uri = uri[:8] + 'ql' + uri[8:]
#     print (uri)
#     return uri

class Config:
    FLASK_APP = os.environ.get('FLASK_APP')
    FLASK_ENV = os.environ.get('FLASK_ENV')
    SECRET_KEY = os.environ.get('SECRET_KEY')
    SQLALCHEMY_DATABASE_URI = os.environ.get('SQLALCHEMY_DATABASE_URI')
    SQLALCHEMY_TRACK_MODIFICATIONS = False