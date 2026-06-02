from pessoa import Pessoa
from datetime import date


class Paciente(Pessoa):
    def __init__(
        self, nome: str, cpf: str, celular: str, data_nascimento: date
    ) -> None:
        super().__init__(nome, cpf, celular)
        self.__data_nascimento = data_nascimento

    @property
    def data_nascimento(self) -> date:
        return self.__data_nascimento

    @data_nascimento.setter
    def data_nascimento(self, data_nascimento: date) -> None:
        self.__data_nascimento = data_nascimento

    def calcular_idade(self):
        nascimento = self.__data_nascimento
        hoje = date.today()

        # calcular a idade baseada no ano que estamos
        idade = hoje.year - nascimento.year

        # verificação se o aniversário já ocorreu este ano
        if hoje.month < nascimento.month or (
            hoje.month == nascimento.month and hoje.day < nascimento.day
        ):
            idade -= 1

        return idade
