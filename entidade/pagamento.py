from abc import abstractmethod, ABC
from datetime import date

from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from entidade.atendimento import Atendimento
#Onde tiver Atendimento colocar "Atendimento"


class Pagamento(ABC):
    def __init__(self, codigo: int,  data: date, valor_pago: float, atendimento: "Atendimento") -> None:
        self.__codigo = codigo
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
    def atendimento(self) -> "Atendimento":
        return self.__atendimento
    
    @property
    def paciente(self):
        return self.__atendimento.paciente
    
    @property
    def codigo(self) -> int:
        return self.__codigo

    @data.setter
    def data(self, data) -> None:
        self.__data = data

    @valor_pago.setter
    def valor_pago(self, valor_pago) -> None:
        self.__valor_pago = valor_pago
    
    @atendimento.setter
    def atendimento(self, atendimento) -> None:
        self.__atendimento = atendimento
    
    @codigo.setter
    def codigo(self, codigo) -> None:
        self.__codigo = codigo

    @abstractmethod
    def processar_pagamento(self) -> None:
        pass
