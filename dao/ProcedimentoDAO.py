from dao.DAO import DAO
from entidade.procedimento import Procedimento


class ProcedimentoDAO(DAO):
    def __init__(self):
        super().__init__('procedimentos.pkl')

    def add(self, procedimento: Procedimento):
        if isinstance(procedimento, Procedimento) and isinstance(procedimento.descricao, str) and procedimento is not None:
            super().add(procedimento.descricao, procedimento)

    def update(self, procedimento: Procedimento, descricao_antiga: str):
        if isinstance(procedimento, Procedimento) and isinstance(procedimento.descricao, str) and procedimento is not None:
            if descricao_antiga != procedimento.descricao:
                self.remove(descricao_antiga)

            super().update(procedimento.descricao, procedimento)

    def get(self, descricao: str):
        if isinstance(descricao, str):
            return super().get(descricao)
        return None

    def remove(self, descricao: str):
        if isinstance(descricao, str):
            super().remove(descricao)
