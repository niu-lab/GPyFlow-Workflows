import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
WORKFLOWS_DIR = os.path.join(BASE_DIR, "workflows")
dbpath = os.path.join(BASE_DIR, "data.sqlite3")
# SQLALCHEMY_DATABASE_URI = 'sqlite:///' + dbpath
WHOOSHEE_MIN_STRING_LEN = 1
SECRET_KEY = 'secret_key'
SQLALCHEMY_DATABASE_URI = "mysql+pymysql://workflow:{passwd}@localhost:{port}/workflows".format(
    passwd=os.environ.get("WORKFLOW_PASSWD"), port=os.environ.get("MYSQL_PORT"))
SQLALCHEMY_TRACK_MODIFICATIONS = True
SQLALCHEMY_COMMIT_TEARDOWN = True
SQLALCHEMY_COMMIT_ON_TEARDOWN = True
