from datetime import date
from entidade.pagamento import Pagamento


class Dinheiro(Pagamento):
    def __init__(self, data: date, valor_pago: float, atendimento) -> None:
        super().__init__(data, valor_pago, atendimento)

    def processar_pagamento(self) -> None:
        print("Pagamento via dinheiro está sendo processado")
