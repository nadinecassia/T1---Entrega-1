from pessoa import Pessoa
from datetime import date


class Paciente (Pessoa):
    def __init__(self, nome: str, cpf: str, celular: str, data_nascimento: date) -> None:
        super().__init__(nome, cpf, celular)
        self.__data_nascimento = data_nascimento
    
     @property
    def data_nascimento(self):
        return self.__data_nascimento
    
    @data_nascimento.setter
    def data_nascimento(self, data_nascimento):
        self.__data_nascimento = data_nascimento