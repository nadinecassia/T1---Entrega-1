from abc import abstractmethod, ABC


class Pessoa(ABC):
    def __init__(self, nome: str, cpf: str, celular: str) -> None:
        self.__nome = nome
        self.__cpf = cpf
        self.__celular = celular

    @property
    def nome(self):
        return self.__nome

    @property
    def cpf(self):
        return self.__cpf

    @property
    def celular(self):
        return self.__celular

    @nome.setter
    def nome(self, nome: str) -> None:
        self.__nome = nome

    @cpf.setter
    def cpf(self, cpf: str) -> None:
        self.__cpf = cpf

    @celular.setter
    def celular(self, celular: str) -> None:
        self.__celular = celular
