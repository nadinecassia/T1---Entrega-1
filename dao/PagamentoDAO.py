from dao.DAO import DAO
from entidade.pagamento import Pagamento


class PagamentoDAO(DAO):
    def __init__(self):
        super().__init__("pagamentos.pkl")

    def add(self, pagamento: Pagamento):
        if (
            (isinstance(pagamento.codigo, int))
            and (pagamento is not None)
            and isinstance(pagamento, Pagamento)
        ):
            super().add(pagamento.codigo, pagamento)

    def update(self, pagamento: Pagamento):
        if (
            (isinstance(pagamento.codigo, int))
            and (pagamento is not None)
            and isinstance(pagamento, Pagamento)
        ):
            super().update(pagamento.codigo, pagamento)
    
    def get(self, key: int):
        if isinstance(key, int):
            return super().get(key)

    def remove(self, key: int):
        if isinstance(key, int):
            return super().remove(key)
