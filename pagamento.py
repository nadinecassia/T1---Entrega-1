from abc import abstractmethod, ABC
from datetime import date


class Pagamento(ABC):
    def __init__(self, data: date, valor_pago: float) -> None:
        super().__init__()
        self.__data = data
        self.__valor_pago = valor_pago

    @property
    def data(self):
        return self.__data
    
    @property
    def valor_pago(self):
        return self.__valor_pago
    
    @data.setter
    def data(self, data):
        self.__data = data
    
    @valor_pago.setter
    def valor_pago(self, valor_pago):
        self.__valor_pago = valor_pago