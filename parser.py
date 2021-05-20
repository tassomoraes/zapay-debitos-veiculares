class SPParser:
    def __init__(self, data):
        self.data = data

    def collect_ipva_debts(self):
        debts = self.get_debts_from_json('IPVAs')

        if debts is not None:
            debts = debts['IPVA']

        else:
            return []

        collection = []

        for debt in debts:
            year = debt.get('Exercicio')
            description = f"IPVA {debt.get('Exercicio')}"
            installment = debt.get('Cota', None)
            title = "- Cota " \
                    f"{'Única' if installment in [7, 8, 0] else installment}"

            to_collection = {
                'amount': float(debt.get('Valor'))/100,
                'description': description,
                'title': f"IPVA {title}",
                'type': 'ipva',
                'year': year,
            }

            if installment is not None:
                to_collection['installment'] = 'unique' if installment in \
                                                [0, 7, 8] else installment

            collection.append(to_collection)

        return collection

    def collect_ticket_debts(self):
        debts = self.get_debts_from_json('Multas')

        if debts is None:
            return []

        debts = debts['Multa']

        collection = []

        for debt in debts:
            to_collection = {
                'amount': float(debt.get('Valor'))/100,
                'auto_infraction': debt.get('AIIP'),
                'description': debt.get('DescricaoEnquadramento'),
                'title': 'Infração de Trânsito',
                'type': "ticket",
            }

            collection.append(to_collection)

        return collection

    def collect_insurance_debts(self):
        debts = self.get_debts_from_json('DPVATs')

        if debts is not None:
            debts = debts['DPVAT']

        else:
            return []

        collection = []

        for debt in debts:
            to_collection = {
                'amount': float(debt.get('Valor'))/100,
                'description': debt.get(
                    'DescricaoServico',
                    f"DPVAT {debt['Exercicio']}"
                ),
                'title': 'Seguro Obrigatório',
                'type': 'insurance',
                'year': debt.get('Exercicio'),
            }

            collection.append(to_collection)

        return collection

    def collect_ipva_debts(self):
        debts = self.get_debts_from_json('IPVAs')

        if debts is not None:
            debts = debts['IPVA']

        else:
            return []

        collection = []

        for debt in debts:
            year = debt.get('Exercicio')
            description = f"IPVA {debt.get('Exercicio')}"
            installment = debt.get('Cota', None)
            title = "- Cota " \
                    f"{'Única' if installment in [7, 8, 0] else installment}"

            to_collection = {
                'amount': float(debt.get('Valor'))/100,
                'description': description,
                'title': f"IPVA {title}",
                'type': 'ipva',
                'year': year,
            }

            if installment is not None:
                to_collection['installment'] = 'unique' if installment in \
                                                [0, 7, 8] else installment

            collection.append(to_collection)

        return collection

    def get_debts_from_json(self, category):
        try:
            return self.data[category]

        except KeyError:
            return None
