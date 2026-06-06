from abc import abstractmethod, ABC
from datetime import date
from entidade.atendimento import Atendimento


class Pagamento(ABC):
    def __init__(self, data: date, valor_pago: float, atendimento: Atendimento) -> None:
        self.__data = data
        self.__valor_pago = valor_pago
        self.__atendimento = atendimento

    @property
    def data(self) -> date:
        return self.__data

    @property
    def valor_pago(self) -> float:
        return self.__valor_pago
    
    @property
    def atendimento(self) -> Atendimento:
        return self.__atendimento
    
    @property
    def paciente(self):
        return self.__atendimento.paciente

    @data.setter
    def data(self, data) -> None:
        self.__data = data

    @valor_pago.setter
    def valor_pago(self, valor_pago) -> None:
        self.__valor_pago = valor_pago
    
    @atendimento.setter
    def atendimento(self, atendimento) -> None:
        self.__atendimento = atendimento

    @abstractmethod
    def processar_pagamento(self) -> None:
        pass
