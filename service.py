from api import API


class SPService:
    """
    Conecta com o webservice do Detran-SP.
    """

    def __init__(self, **kwargs):
        """
        Construtor.
        """

        self.params = kwargs

    def get_json_response(self, method):
        """
        Pega a resposta da requisição em json.
        """
        api = API(self.params["license_plate"], self.params["renavam"], method)
        return api.fetch()

    def debt_search(self):
        """
        Pega os débitos de acordo com a opção passada.
        """

        if self.params['debt_option'] == 'ticket':
            response_json = self.get_json_response("ConsultaMultas")

        elif self.params['debt_option'] == 'ipva':
            response_json = self.get_json_response("ConsultaIPVA")

        elif self.params['debt_option'] == 'dpvat':
            response_json = self.get_json_response("ConsultaDPVAT")

        else:
            raise Exception("opção inválida")

        debts = {
            'IPVAs': response_json.get('IPVAs') or {},
            'DPVATs': response_json.get('DPVATs') or {},
            'Multas': response_json.get('Multas') or {},
        }

        for debt in debts:
            if debts[debt] == {}:
                debts[debt] = None

        return debts
