import os

base_dir = os.path.dirname(os.path.abspath(__file__))
dbpath = os.path.join(base_dir, "data.sqlite3")
WORKFLOWS_DIR = os.path.join(base_dir, "workflows")
SQLALCHEMY_DATABASE_URI = 'sqlite:///' + dbpath
SQLALCHEMY_TRACK_MODIFICATIONS = True
