from app.keys import secret_key
from jogoteca import app
from app.credentials import get_pass
import os


app.secret_key = secret_key()
MYSQL_HOST = "127.0.0.1"
MYSQL_USER = "root"
MYSQL_PASSWORD = get_pass()
MYSQL_DB = 'jogoteca'
MSQYL_PORT = 3306
UPLOAD_PATH = os.path.dirname(os.path.abspath(__file__)) + '/uploads'