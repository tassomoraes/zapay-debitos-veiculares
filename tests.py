from service import SPService

# Sinta-se livre para deletar o teste abaixo, caso queira.
def test_search_ticket():
    service = SPService(
        license_plate="license_plate",
        renavam="renavam",
        debt_option="ticket"
    )
    result = service.debt_search()
    assert result == True