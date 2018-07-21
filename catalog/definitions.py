import os


CATALOG_DIR = os.path.dirname(os.path.abspath(__file__))
ROOT_DIR = os.path.abspath(os.path.join(CATALOG_DIR, '..'))
SECRET_DIR = os.path.join(ROOT_DIR, 'secret')
GOOGLE_SECRET = os.path.join(SECRET_DIR, 'google/client_secret.json')