import os

SECRET_KEY = 'alura'

SQLALCHEMY_DATABASE_URI = \
    '{SGBD}://{usuario}:{senha}@{servidor}/{database}'.format(
        SGBD = 'mysql+mysqlconnector',
        usuario = 'root',
        senha = '88428666',
        servidor = 'localhost',
        database = 'projetos'

    )

UPLOAD_PATH = os.path.dirname(os.path.abspath(__file__)) + '/uploads'