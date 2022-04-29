from sql_alchemy import banco


class PessoaModel(banco.Model):

    __tablename__ = 'pessoas'

    id_pessoa = banco.Column(banco.Integer, primary_key=True)
    nome = banco.Column(banco.String(100), nullable=False)
    rg = banco.Column(banco.String(100), nullable=False, unique=True)
    cpf = banco.Column(banco.String(100), nullable=False, unique=True)
    data_nascimento = banco.Column(banco.Date, nullable=False)
    data_admissao = banco.Column(banco.Date, nullable=False)
    funcao = banco.Column(banco.String(100), nullable=True)

    def __init__(self, nome, rg, cpf, data_nascimento,
                 data_admissao, funcao):
        self.nome = nome
        self.rg = rg
        self.cpf = cpf
        self.data_nascimento = data_nascimento
        self.data_admissao = data_admissao
        self.funcao = funcao

    def converte_json(self):
        return {
            'id_pessoa': self.id_pessoa,
            'nome': self.nome,
            'rg': self.rg,
            'cpf': self.cpf,
            'data_nascimento': str(self.data_nascimento),
            'data_admissao': str(self.data_admissao),
            'funcao': self.funcao
        }

    @classmethod
    def get_pessoas(objeto_pessoa):
        pessoas = objeto_pessoa.query.all()

        if not pessoas:
            return None
        return pessoas

    @classmethod
    def get_pessoa(objeto_pessoa, id_pessoa: int):
        pessoa = objeto_pessoa.query.filter_by(id_pessoa=id_pessoa).first()

        if not pessoa:
            return None
        return pessoa

    def post_pessoa(self):
        banco.session.add(self)
        banco.session.commit()

    def put_pessoa(self, **kwargs):
        self.nome = kwargs.get('nome')
        self.rg = kwargs.get('rg')
        self.cpf = kwargs.get('cpf')
        self.data_nascimento = kwargs.get('data_nascimento')
        self.data_admissao = kwargs.get('data_admissao')
        self.funcao = kwargs.get('funcao')

    def delete_pessoa(self):
        banco.session.delete(self)
        banco.session.commit()
