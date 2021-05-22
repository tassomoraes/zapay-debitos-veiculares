from service import SPService

# Sinta-se livre para deletar o teste abaixo, caso queira.
def test_search_ticket():
    service = SPService(
        license_plate="ABC1234",
        renavam="11111111111",
        debt_option="licensing"
    )
    result = service.debt_search()
    assert result == True