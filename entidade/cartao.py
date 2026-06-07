from datetime import date
from entidade.pagamento import Pagamento


class Cartao(Pagamento):
    def __init__(
        self,
        data: date,
        valor_pago: float,
        numero_cartao: str,
        bandeira: str,
        atendimento,
    ) -> None:
        super().__init__(data, valor_pago, atendimento)
        self.__numero_cartao = numero_cartao
        self.__bandeira = bandeira

    @property
    def numero_cartao(self) -> str:
        return self.__numero_cartao

    @property
    def bandeira(self) -> str:
        return self.__bandeira

    @numero_cartao.setter
    def numero_cartao(self, numero_cartao) -> None:
        self.__numero_cartao = numero_cartao

    @bandeira.setter
    def bandeira(self, bandeira) -> None:
        self.__bandeira = bandeira

    def processar_pagamento(self) -> None:
        print(f"Pagamento no cartão {self.__bandeira} está sendo processado")
