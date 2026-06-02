from datetime import date
from pagamento import Pagamento


class Pix(Pagamento):
    def __init__(self, data: date, valor_pago: float, cpf_pagador: str) -> None:
        super().__init__(data, valor_pago)
        self.__cpf_pagador = cpf_pagador

    @property
    def cpf_pagador(self):
        return self.__cpf_pagador

    @cpf_pagador.setter
    def cpf_pagador(self, cpf_pagador):
        self.__cpf_pagador = cpf_pagador
