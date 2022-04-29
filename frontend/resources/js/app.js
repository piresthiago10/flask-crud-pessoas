Vue.use(VueMask.VueMaskPlugin);
const app = new Vue({
    el: '#app',
    data: {
        apiUrl: 'http://127.0.0.1:5000/',

        error: false,
        errorMessage: '',
        success: false,
        successMessage: '',

        isUpdate: false,

        pessoas: [],
        responsePessoasData: [],
        responsePessoaData: '',
        pessoa: {
            idPessoa: '',
            nome: '',
            rg: '',
            cpf: '',
            dataNascimento: '',
            dataAdmissao: '',
            funcao: '',
        },
    },
    filters: {
        dataAdmissao: function (value) {
            dataAdmissaoFormatoBrasileiro = value.split("-")
            return dataAdmissaoFormatoBrasileiro[2] + "/" + dataAdmissaoFormatoBrasileiro[1] + "/" + dataAdmissaoFormatoBrasileiro[0]
        },
        primeiroNome: function (value) {
            nomePessoa = value.split(" ")
            return nomePessoa[0]
        }
    },
    methods: {
        informaErro: function (mensagemErro) {
            this.error = true
            this.errorMessage = mensagemErro
            setTimeout(() => { this.error = '' }, 5000);
            setTimeout(() => { this.errorMessage = '' }, 5000);
        },
        informaSucesso: function (mensagemSucesso) {
            this.success = true
            this.successMessage = mensagemSucesso
            setTimeout(() => { this.success = '' }, 5000);
            setTimeout(() => { this.successMessage = '' }, 5000);
        },
        validaPessoa: function () {
            if (!this.pessoa.nome) {
                this.informaErro('Campo Nome Completo vazio')
            }
            else if (!this.pessoa.rg) {
                this.informaErro('Campo RG vazio')
            }
            else if (!this.pessoa.cpf) {
                this.informaErro('Campo CPF vazio')
            }
            else if (!this.pessoa.dataNascimento) {
                this.informaErro('Campo Data de Nascimento vazio')
            }
            else if (!this.pessoa.dataAdmissao) {
                this.informaErro('Campo Data de Admissão vazio')
            }
            else {
                this.error = false
            }
        },
        removeEspacosDoComecoEFimDeString: function (string) {
            if (string) {
                return string.trim()
            }
        },
        getPessoas: async function () {
            this.responsePessoasData = []
            this.pessoas = []
            try {
                await axios.get(this.apiUrl + 'pessoas', {
                })
                    .then(response => (this.responsePessoasData = response.data))
                for (let i = 0; i < this.responsePessoasData.pessoas.length; i++) {
                    this.pessoas.push({
                        'idPessoa': this.responsePessoasData.pessoas[i].id_pessoa,
                        'nome': this.responsePessoasData.pessoas[i].nome,
                        'dataAdmissao': this.responsePessoasData.pessoas[i].data_admissao,
                    })
                }
            } catch (err) {
                this.informaErro('Não foi possível obter as pessoas. Consulte o nosso atendimento para mais detalhes.')
            }
        },
        getPessoa: async function (id_pessoa) {
            try {
                await axios.get(this.apiUrl + 'pessoas/' + id_pessoa, {
                })
                    .then(response => (this.responsePessoaData = response.data.pessoa))
                this.pessoa.idPessoa = this.responsePessoaData.id_pessoa
                this.pessoa.nome = this.responsePessoaData.nome
                this.pessoa.rg = this.responsePessoaData.rg
                this.pessoa.cpf = this.responsePessoaData.cpf
                this.pessoa.dataNascimento = this.responsePessoaData.data_nascimento
                this.pessoa.dataAdmissao = this.responsePessoaData.data_admissao
                this.pessoa.funcao = this.responsePessoaData.funcao
                this.isUpdate = true
            } catch (error) {
                this.informaErro('Não foi possível obter os dados da pessoa. Consulte o nosso atendimento para mais detalhes.')
            }
        },
        postPessoa: async function () {
            this.validaPessoa()
            data = {
                "nome": this.removeEspacosDoComecoEFimDeString(this.pessoa.nome),
                "rg": this.pessoa.rg,
                "cpf": this.pessoa.cpf,
                "data_nascimento": this.pessoa.dataNascimento,
                "data_admissao": this.pessoa.dataAdmissao,
                "funcao": this.removeEspacosDoComecoEFimDeString(this.pessoa.funcao)
            }
            console.log(data)
            try {
                if (this.error == false) {
                    await axios.post(this.apiUrl + 'pessoas', data)
                    this.informaSucesso("Pessoa cadastrada com Sucesso!")
                    this.limparFormulario()
                    this.getPessoas()
                }
            } catch (error) {
                console.log(error)
                this.informaErro('Não foi possível realizar o cadastro. Consulte o nosso atendimento para mais detalhes.')
            }
        },
        putPessoa: async function () {
            this.validaPessoa()
            data = {
                "nome": this.removeEspacosDoComecoEFimDeString(this.pessoa.nome),
                "rg": this.pessoa.rg,
                "cpf": this.pessoa.cpf,
                "data_nascimento": this.pessoa.dataNascimento,
                "data_admissao": this.pessoa.dataAdmissao,
                "funcao": this.removeEspacosDoComecoEFimDeString(this.pessoa.funcao)
            }
            try {
                if (this.error == false) {
                    await axios.put(this.apiUrl + 'pessoas/' + this.pessoa.idPessoa, data)
                    this.informaSucesso("Pessoa atualizada com Sucesso!")
                    this.limparFormulario()
                    this.getPessoas()
                }
            } catch (error) {
                this.informaErro('Não foi possível atualizar o cadastro. Consulte o nosso atendimento para mais detalhes.')
            }
        },
        deletePessoa: async function (id_pessoa) {
            try {
                let opcaoSelecionada = confirm("Deseja realmente excluir a pessoa?");
                if (opcaoSelecionada == true) {
                    await axios.delete(this.apiUrl + 'pessoas/' + id_pessoa)
                    this.informaSucesso("Pessoa excluída com Sucesso!")
                    this.getPessoas()
                }
                else {
                    this.informaSucesso("Pessoa não foi excluída!")
                    this.getPessoas()
                }

            } catch (error) {
                this.informaErro('Não foi possível excluir o cadastro. Consulte o nosso atendimento para mais detalhes.')
            }

        },
        limparFormulario: function () {
            this.pessoa.idPessoa = ''
            this.pessoa.nome = ''
            this.pessoa.rg = ''
            this.pessoa.cpf = ''
            this.pessoa.dataNascimento = ''
            this.pessoa.dataAdmissao = ''
            this.pessoa.funcao = ''
            this.isUpdate = false
        },
    },
    async created() {
        await this.getPessoas()
    }
})
