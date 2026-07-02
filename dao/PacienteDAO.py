from dao.DAO import DAO
from entidade.paciente import Paciente


class PacienteDAO(DAO):
    def __init__(self):
        super().__init__("pacientes.pkl")

    def add(self, paciente: Paciente):
        if (
            (isinstance(paciente.cpf, str))
            and (paciente is not None)
            and isinstance(paciente, Paciente)
        ):
            super().add(paciente.cpf, paciente)

    def update(self, paciente: Paciente):
        if (
            (isinstance(paciente.cpf, str))
            and (paciente is not None)
            and isinstance(paciente, Paciente)
        ):
            super().update(paciente.cpf, paciente)
    
    def get(self, key: str):
        if isinstance(key, str):
            return super().get(key)

    def remove(self, key: str):
        if isinstance(key, str):
            return super().remove(key)
