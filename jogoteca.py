from flask import Flask
from flask_mysqldb import MySQL

#obj app gets all config from the application
app = Flask(__name__)
app.config.from_pyfile('config.py')

#db obj is initiated by MySQL class obj. The db obj is assigned all the config from the app
db = MySQL(app)

#importar as view somente depois das criacoes do DB e da Aplicacao. View depende de db e app. Se chamarmos view no topo
#aplicacao havera um erro pois app e db ainda nao existem.
from views import *

if __name__ == '__main__':
    # app.run(host='0.0.0.0', port=8080)
    app.run(debug=True)
