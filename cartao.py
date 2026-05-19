from datetime import date
from pagamento import Pagamento


class Cartao(Pagamento):
    def __init__(self, data: date, valor_pago: float, numero_cartao: str, bandeira: str) -> None:
        super().__init__(data, valor_pago)
        self.__numero_cartao = numero_cartao
        self.__bandeira = bandeira

    @property
    def numero_cartao(self):
        return self.__numero_cartao
    
    @property
    def bandeira(self):
        return self.__bandeira
    
    @numero_cartao.setter
    def numero_cartao(self, numero_cartao):
        self.__numero_cartao = numero_cartao

    @bandeira.setter
    def bandeira(self, bandeira):
        self.__bandeira = bandeira