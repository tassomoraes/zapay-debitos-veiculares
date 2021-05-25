import pytest

# devido a um ImportError no pytest foi criado uma cópia do arquivo
# parser, parsertest, para processeguir com os testes nos métodos
# do arquivo parser
from parsertest import SPParser
from service import SPService

licensing = {
                "Servico": "Licenciamento",
                "Veiculo": {
                    "UF": "SP",
                    "Placa": "ABC1234",
                    "CPFCNPJ": "000.000.000-00",
                    "Renavam": "11111111111",
                    "Proprietario": "JOHN",
                },
                "Exercicio": 2021,
                "TaxaLicenciamento": 9891
            }
dpvats = {
    "DPVAT": [
        {
            "Valor": 523,
            "Exercicio": 2020,
        }
    ]
}
multas = {
    "Multa": [
        {
            "AIIP": "5E5E5E5E  ",
            "Guia": 472535212,
            "Valor": 20118,
            "DescricaoEnquadramento": "Estacionar em Desacordo"
                                      " com a Sinalizacao."
        },
        {
            "AIIP": "6F6F6F6F  ",
            "Valor": 13166,
            "DescricaoEnquadramento": "Trans. Veloc. Super. a"
                                      " Maxima Permitida"
                                      "em Ate 20%."
        }
    ]
}
ipvas = {
    "IPVA": [
        {
            "Cota": 8,
            "Valor": 136569,
            "Exercicio": 2021,
        },
        {
            "Cota": 2,
            "Valor": 101250,
            "Exercicio": 2020,
        }
    ]
}

def service(debt_option):
    return SPService(
        license_plate="ABC1C34",
        renavam="11111111111",
        debt_option=debt_option
    )

def debts(ipva,dpvat,multa,licenc):
    return {
        'IPVAs': ipva,
        'DPVATs': dpvat,
        'Multas': multa,
        'Licenciamento': licenc
    }

# Testes para service
# Testa diversas buscas com debt_option
@pytest.mark.parametrize(
    "service, debts",
    [(service("ipva"),debts(ipvas,None,None,None)),
                          (service("dpvat"),debts(None,dpvats,None,None)),
                          (service("ticket"),debts(None,None,multas,None)),
                          (service("licensing"),debts(None,None,None,licensing)),
                          (service("ipva ticket"),debts(ipvas,None,multas,None)),
                          (service("ticket ipva"),debts(ipvas,None,multas,None)),
                          (service("ipva licensing dpvat"),debts(ipvas,dpvats,None,licensing)),
                          (service("ipva ticket licensing dpvat"),debts(ipvas,dpvats,multas,licensing))]
)
def test_search_ticket(service,debts):
    result = service.debt_search()
    assert result == debts

def test_search_ticket_opcao_invalida():
    serv = service("invalido")
    with pytest.raises(Exception):
        serv.debt_search()

consulta_licenciamento = {
                "Servico": "Licenciamento",
                "Veiculo": {
                    "UF": "SP",
                    "Placa": "ABC1234",
                    "CPFCNPJ": "000.000.000-00",
                    "Renavam": "11111111111",
                    "Proprietario": "JOHN",
                },
                "Exercicio": 2021,
                "TaxaLicenciamento": 9891
            }

def test_get_json_response():
    serv = service("licensing")
    assert serv.get_json_response("ConsultaLicenciamento") == consulta_licenciamento

# Testes para Parser
collection_ipva = [
    {
        'amount': 1365.69,
        'description': 'IPVA 2021',
        'title': 'IPVA - Cota Única',
        'type': 'ipva',
        'year': 2021,
        'installment': 'unique'
    },
    {
        'amount': 1012.50,
        'description': 'IPVA 2020',
        'title': 'IPVA - Cota 2',
        'type': 'ipva',
        'year': 2020,
        'installment': 2
    }
]
collection_multas = [
    {
        'amount': 201.18,
        'auto_infraction': '5E5E5E5E  ',
        'description': 'Estacionar em Desacordo'
                       ' com a Sinalizacao.',
        'title': 'Infração de Trânsito',
        'type': "ticket",
    },
    {
        'amount': 131.66,
        'auto_infraction': '6F6F6F6F  ',
        'description': 'Trans. Veloc. Super. a'
                       ' Maxima Permitida'
                       'em Ate 20%.',
        'title': 'Infração de Trânsito',
        'type': "ticket",
    }
]

@pytest.fixture
def parser_all_debts():
    parser = SPParser(debts(ipvas,dpvats,multas,licensing))
    return parser

# Foi preciso transformar o json em string para remover os \n
def test_collect_ipva_debts(parser_all_debts):
    parser = parser_all_debts.collect_ipva_debts()
    str_parser = str(parser).replace('\n',"")
    assert str_parser == str(collection_ipva)

def test_collect_ticket_debts(parser_all_debts):
    parser = parser_all_debts.collect_ticket_debts()
    str_parser = str(parser).strip('\n')
    assert str_parser == str(collection_multas)

