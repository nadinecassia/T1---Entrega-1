from dao.DAO import DAO
from entidade.TipoAtendimento import TipoAtendimento


class TipoAtendimentoDAO(DAO):
    def __init__(self):
        super().__init__("tipos_atendimentos.pkl")

    def add(self, tipo_atendimento: TipoAtendimento):
        if (
            (isinstance(tipo_atendimento.codigo, int))
            and (tipo_atendimento is not None)
            and isinstance(tipo_atendimento, TipoAtendimento)
        ):
            super().add(tipo_atendimento.codigo, tipo_atendimento)

    def update(self, tipo_atendimento: TipoAtendimento):
        if (
            (isinstance(tipo_atendimento.codigo, int))
            and (tipo_atendimento is not None)
            and isinstance(tipo_atendimento, TipoAtendimento)
        ):
            super().update(tipo_atendimento.codigo, tipo_atendimento)
    
    def get(self, key: int):
        if isinstance(key, int):
            return super().get(key)

    def remove(self, key: int):
        if isinstance(key, int):
            return super().remove(key)
