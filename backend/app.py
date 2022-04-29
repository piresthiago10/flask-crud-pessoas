from flask import Flask
from flask_restful import Api

from resources.pessoas import Pessoa, Pessoas

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = "mysql://thiagosantos:dGhpYWdvc2Fu@" \
    "jobs.visie.com.br:3306/thiagosantos"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
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
