from flask import Flask
from flask_restful import Api

from resources.pessoas import Pessoa, Pessoas

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///banco.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['JWT_SECRET_KEY'] = 'DontTellAnyone'
app.config['JWT_BLACKLIST_ENABLED'] = True
api = Api(app)


@app.before_first_request
def cria_banco():
    banco.create_all()


api.add_resource(Pessoas, '/pessoas', methods=["GET", "POST"])
api.add_resource(Pessoa, '/pessoas/<int:id_pessoa>',
                 methods=["GET", "PUT", "DELETE"])

if __name__ == '__main__':
    from sql_alchemy import banco
    banco.init_app(app)
    app.run(debug=True)
