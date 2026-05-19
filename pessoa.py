from abc import abstractmethod, ABC


class Pessoa(ABC):
    def __init__(self, nome: str, cpf: str, celular: str) -> None:
        super().__init__()
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
    def nome(self, nome):
        self.__nome = nome
    
    @cpf.setter
    def cpf(self, cpf):
        self.__cpf = cpf

    @celular.setter
    def celular(self, celular):
        self.__celular = celular
    