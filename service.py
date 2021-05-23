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

    def plate_translated(self, plate):
        """
        Traduz placas do Mercosul para placas antigas
        """
        letter = plate[4]

        translate_table = {
            'A': '0', 'B': '1',
            'C': '2', 'D': '3',
            'E': '4', 'F': '5',
            'G': '6', 'H': '7',
            'I': '8', 'J': '9'
        }

        #muda somente a letra na posição 4
        old_plate = plate[:4] + translate_table.get(letter) + plate[5:]
        return old_plate

    def get_json_response(self, method):
        """
        Pega a resposta da requisição em json.
        """
        recived_plate = self.params["license_plate"]

        if recived_plate[4] in ['A','B','C','D','E','F','G','H','I','J']:
            plate = self.plate_translated(recived_plate)
        else:
            plate = recived_plate

        api = API(plate, self.params["renavam"], method)
        return api.fetch()

    def debt_search(self):
        """
        Pega os débitos de acordo com a opção passada.
        """

        response_json = {}
        #verificação para várias opções
        valid = False   #validade da opção

        if 'ticket' in self.params['debt_option']:
            response_json['ticket'] = self.get_json_response("ConsultaMultas")
            valid = True

        if 'ipva' in self.params['debt_option']:
            response_json['ipva'] = self.get_json_response("ConsultaIPVA")
            valid = True

        if 'dpvat' in self.params['debt_option']:
            response_json['dpvat'] = self.get_json_response("ConsultaDPVAT")
            valid = True

        if 'licensing' in self.params['debt_option']:
            response_json['licensing'] = self.get_json_response("ConsultaLicenciamento")
            valid = True

        if valid is not True:
            raise Exception("opção inválida")

        response_json_ipva = response_json.get('ipva', None)
        response_json_dpvat = response_json.get('dpvat', None)
        response_json_ticket = response_json.get('ticket', None)
        response_json_licensing = response_json.get('licensing', None)

        if response_json_ipva is not None:
            ipvas = response_json_ipva.get('IPVAs') or {}
        else:
            ipvas = {}

        if response_json_dpvat is not None:
            dpvats = response_json_dpvat.get('DPVATs') or {}
        else:
            dpvats = {}

        if response_json_ticket is not None:
            multas = response_json_ticket.get('Multas') or {}
        else:
            multas = {}

        if response_json_licensing is not None:
            licenciamento = response_json_licensing or {}
        else:
            licenciamento = {}

        debts = {
            'IPVAs': ipvas,
            'DPVATs': dpvats,
            'Multas': multas,
            'Licenciamento': licenciamento
        }

        for debt in debts:
            if debts[debt] == {}:
                debts[debt] = None

        return debts
