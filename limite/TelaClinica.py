from limite.AbstractTela import AbstractTela
from datetime import datetime


class TelaClinica(AbstractTela):
    def __init__(self, controlador):
        super().__init__(controlador)

    def mostrar_menu(self) -> int:
        print("\n-------- CADASTRO CLÍNICAS --------")
        print("1 - Incluir Clínica")
        print("2 - Alterar Clínica")
        print("3 - Excluir Clínica")
        print("4 - Listar Clínicas")
        print("0 - Voltar")

        opcao = self.le_num_inteiro("Escolha a opção: ", [1, 2, 3, 4, 0])
        return opcao

    def pegar_dados(self) -> dict:
        print("\n-------- CADASTRAR / ALTERAR CLÍNICA --------")
        nome = self.le_texto_obrigatorio("Nome da clínica: ")
        descricao = self.le_texto_obrigatorio("Descrição: ")
        cidade = self.le_texto_obrigatorio("Cidade (Localização): ")
        horario_aberto= self.le_horario("Horário de abertura (HH:MM): ")
        horario_fechado= self.le_horario("Horário de fechamento (HH:MM): ")

        return {
            "nome": nome,
            "descricao": descricao,
            "cidade": cidade,
            "horario_aberto": horario_aberto,
            "horario_fechado": horario_fechado,
        }

    def mostrar_clinica(self, dados_clinica: dict):
        print("NOME DA CLÍNICA: ", dados_clinica["nome"])
        print("DESCRIÇÃO: ", dados_clinica["descricao"])
        print("CIDADE: ", dados_clinica["cidade"])
        print("HORÁRIO DE ABERTURA", dados_clinica["horario_aberto"].strftime("%H:%M"))
        print("HORÁRIO DE FECHAMENTO", dados_clinica["horario_fechado"].strftime("%H:%M"))
        print("-" * 30)

    def selecionar(self) -> str:
        print("\n-------- SELECIONAR CLÍNICA --------")
        nome = self.le_texto_obrigatorio("Digite o nome exato da clínica que deseja selecionar: ")
        return nome

    def mostrar_msg(self, msg: str):
        print(msg)
