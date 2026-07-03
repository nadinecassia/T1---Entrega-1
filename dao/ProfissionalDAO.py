from dao.DAO import DAO
from entidade.profissional import Profissional


class ProfissionalDAO(DAO):
    def __init__(self):
        super().__init__("profissionais.pkl")

    def add(self, profissional: Profissional):
        if (
            (isinstance(profissional.cpf, str))
            and (profissional is not None)
            and isinstance(profissional, Profissional)
        ):
            super().add(profissional.cpf, Profissional)

    def update(self, profissional: Profissional):
        if (
            (isinstance(profissional.cpf, str))
            and (profissional is not None)
            and isinstance(profissional, Profissional)
        ):
            super().update(profissional.cpf, Profissional)
    
    def get(self, key: str):
        if isinstance(key, str):
            return super().get(key)

    def remove(self, key: str):
        if isinstance(key, str):
            return super().remove(key)
