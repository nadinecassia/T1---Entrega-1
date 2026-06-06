from datetime import time


class Clinica:
    def __init__(
        self,
        nome: str,
        descricao: str,
        cidade: str,
        horario_aberto: time,
        horario_fechado: time,
    ):
        self.__nome = nome
        self.__descricao = descricao
        self.__cidade = cidade
        self.__horario_aberto = horario_aberto
        self.__horario_fechado = horario_fechado

    @property
    def nome(self) -> str:
        return self.__nome

    @nome.setter
    def nome(self, nome) -> None:
        self.__nome = nome

    @property
    def descricao(self) -> str:
        return self.__descricao

    @descricao.setter
    def descricao(self, descricao) -> None:
        self.__descricao = descricao

    @property
    def cidade(self) -> str:
        return self.__cidade

    @cidade.setter
    def cidade(self, cidade) -> None:
        self.__cidade = cidade

    @property
    def horario_aberto(self) -> time:
        return self.__horario_aberto

    @horario_aberto.setter
    def horario_aberto(self, horario_aberto: time) -> None:
        self.__horario_aberto = horario_aberto

    @property
    def horario_fechado(self) -> time:
        return self.__horario_fechado

    @horario_fechado.setter
    def horario_fechado(self, horario_fechado: time) -> None:
        self.__horario_fechado = horario_fechado

    def esta_aberta(self, horario_inicio: time, horario_fim: time) -> bool:
        return (
            self.__horario_aberto <= horario_inicio
            and horario_fim <= self.__horario_fechado
        )
