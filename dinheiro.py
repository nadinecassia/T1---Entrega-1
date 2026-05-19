from datetime import date
from pagamento import Pagamento


class Dinheiro(Pagamento):
    def __init__(self, data: date, valor_pago: float) -> None:
        super().__init__(data, valor_pago)
        pass
    