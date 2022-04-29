from datetime import datetime

from flask_restful import Resource, inputs, reqparse
from models.pessoa import PessoaModel

from .utils import gera_response


class Pessoas(Resource):
    def get(self):
        pessoas = PessoaModel.get_pessoas()

        if not pessoas:
            return gera_response(404, "pessoas", {},
                                 "Não foram localizadas pessoas.")
        pessoas_json = [pessoa.converte_json() for pessoa in pessoas]
        return gera_response(200, "pessoas", pessoas_json)

    def post(self):
        dados = Pessoa.argumentos.parse_args()
        pessoa = PessoaModel(**dados)
        pessoa_json = pessoa.converte_json()

        try:
            pessoa.post_pessoa()
            return gera_response(201, "pessoa", pessoa_json)
        except Exception:
            return gera_response(500, "pessoa", {},
                                 "Ocorreu um erro interno ao "
                                 "tentar registrar a pessoa.")


class Pessoa(Resource):

    argumentos = reqparse.RequestParser()
    argumentos.add_argument('nome', type=str, required=True,
                            help="O campo 'nome' não pode estar vazio.")
    argumentos.add_argument('rg', type=str, required=True,
                            help="O campo 'rg' não pode estar vazio.")
    argumentos.add_argument('cpf',
                            required=True,
                            type=inputs.regex('^\d{3}\.\d{3}\.\d{3}\-\d{2}$'),
                            help="O campo 'cpf' não pode estar "
                            "vazio ou incorreto.")
    argumentos.add_argument('data_nascimento',
                            type=lambda x: datetime.strptime(
                                x, '%Y-%m-%d'),
                            required=True,
                            help="O campo 'data_nascimento' "
                            "não pode estar vazio ou incorreto.")
    argumentos.add_argument('data_admissao',
                            type=lambda x: datetime.strptime(
                                x, '%Y-%m-%d'),
                            required=True,
                            help="O campo 'data_admissao' "
                            "não pode estar vazio ou incorreto.")
    argumentos.add_argument('funcao', type=str)

    def get(self, id_pessoa: int):
        pessoa = PessoaModel.get_pessoa(id_pessoa)
        pessoa_json = pessoa.converte_json()
        if not pessoa:
            return gera_response(404, "pessoa", {},
                                 "Não foi localizada nenhuma pessoa.")
        return gera_response(200, "pessoa", pessoa_json)

    def put(self, id_pessoa: int):
        dados = Pessoa.argumentos.parse_args()
        pessoa = PessoaModel.get_pessoa(id_pessoa)

        if pessoa:
            try:
                pessoa.put_pessoa(**dados)
                pessoa.post_pessoa()
                pessoa_json = pessoa.converte_json()
                return gera_response(200, "pessoa", pessoa_json)
            except Exception:
                return gera_response(500, "pessoa", {},
                                     "Ocorreu um erro interno ao "
                                     "tentar atualizar a pessoa.")

        return gera_response(404, "pessoa", {},
                             "Não foi localizada nenhuma pessoa.")

    def delete(self, id_pessoa: int):
        pessoa = PessoaModel.get_pessoa(id_pessoa)

        if pessoa:
            try:
                pessoa.delete_pessoa()
                return gera_response(204, "pessoa", {})
            except Exception:
                return gera_response(500, "pessoa", {},
                                     "Ocorreu um erro interno ao "
                                     "tentar excluir a pessoa.")
        return gera_response(404, "pessoa", {},
                             "Não foi localizada nenhuma pessoa.")
