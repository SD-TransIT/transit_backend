import os

from waitress import serve

from transit.wsgi import application

if __name__ == '__main__':
    serve(application, port=os.getenv('PORT', '8000'))
