import sys
import json
from service import SPService
from parser import SPParser

if __name__ == "__main__":

    try:
        debt_option = sys.argv[1]
        license_plate = sys.argv[2]
        renavam = sys.argv[3]
        assert len(sys.argv) == 4
    except (AssertionError, IndexError):
        print("Argumentos inválidos")
        sys.exit(1)

    service = SPService(
        license_plate=license_plate,
        renavam=renavam,
        debt_option=debt_option
    )
    try:
        search_result = service.debt_search()
    except Exception as exc:
        print(exc)
        sys.exit(1)

    parser = SPParser(search_result)

    result = []
    # varificação para várias opções selecionadas
    valid = False  # validade da opção

    if "ticket" in debt_option:
        result.append(parser.collect_ticket_debts())
        valid = True
    if "ipva" in debt_option:
        result.append(parser.collect_ipva_debts())
        valid = True
    if "dpva" in debt_option:
        result.append(parser.collect_insurance_debts())
        valid = True
    if "licensing" in debt_option:
        result.append(parser.collect_licensing_debts())
        valid = True

    if valid is not True:
        print("Opção inválida")
        sys.exit(1)

    print(
        json.dumps(result, indent=4, ensure_ascii=False)
    )
    sys.exit(0)