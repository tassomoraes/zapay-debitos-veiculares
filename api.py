class API:
    vehicles = [
        ("ABC1234", "11111111111"),
    ]

    def __init__(self, license_plate, renavam, debt_option):
        self.debt_option = debt_option

        if (license_plate, renavam) not in self.vehicles:
            raise Exception("veículo não encontrado")

        self.license_plate = license_plate
        self.renavam = renavam

    def fetch(self):
        if self.debt_option == "ConsultaMultas":
            return {
                "Multas": {
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
                },
                "Servico": "Multas",
                "Veiculo": {
                    "UF": "SP",
                    "Placa": "ABC1234",
                    "CPFCNPJ": "000.000.000-00",
                    "Renavam": "11111111111",
                    "Proprietario": "JOHN",
                }
            }
        elif self.debt_option == "ConsultaIPVA":
            return {
                "IPVAs": {
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
                },
                "Servico": "IPVA",
                "Veiculo": {
                    "UF": "SP",
                    "Placa": "ABC1234",
                    "CPFCNPJ": "000.000.000-00",
                    "Renavam": "11111111111",
                    "Proprietario": "JOHN",
                }
            }
        elif self.debt_option == "ConsultaDPVAT":
            return {
                "DPVATs": {
                    "DPVAT": [
                        {
                            "Valor": 523,
                            "Exercicio": 2020,
                        }
                    ]
                },
                "Servico": "DPVAT",
                "Veiculo": {
                    "UF": "SP",
                    "Placa": "ABC1234",
                    "CPFCNPJ": "000.000.000-00",
                    "Renavam": "11111111111",
                    "Proprietario": "JOHN",
                }
            }
        elif self.debt_option == "ConsultaLicenciamento":
            return {
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
        else:
            raise Exception("opção inválida")