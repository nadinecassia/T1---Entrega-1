from dao.DAO import DAO
from entidade.clinica import Clinica


class ClinicaDAO(DAO):
    def __init__(self):
        super().__init__('clinicas.pkl')

    def add(self, clinica: Clinica):
        if isinstance(clinica, Clinica) and isinstance(clinica.nome, str) and clinica is not None:
            super().add(clinica.nome, clinica)

    def update(self, clinica: Clinica):
        if isinstance(clinica, Clinica) and isinstance(clinica.nome, str) and clinica is not None:
            super().update(clinica.nome, clinica)

    def get(self, nome: str):
        if isinstance(nome, str):
            return super().get(nome)
        return None

    def remove(self, nome: str):
        if isinstance(nome, str):
            super().remove(nome)
