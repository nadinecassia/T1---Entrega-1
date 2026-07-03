from datetime import date
from entidade.pagamento import Pagamento


class Pix(Pagamento):
    def __init__(
        self, codigo: int, data: date, valor_pago: float, cpf_pagador: str, atendimento
    ) -> None:
        super().__init__(codigo, data, valor_pago, atendimento)
        self.__cpf_pagador = cpf_pagador

    @property
    def cpf_pagador(self):
        return self.__cpf_pagador

    @cpf_pagador.setter
    def cpf_pagador(self, cpf_pagador) -> None:
        self.__cpf_pagador = cpf_pagador

    def processar_pagamento(self) -> None:
        print(
            f"Pagamento via PIX está sendo processado. CPF do pagador: {self.__cpf_pagador}"
        )
