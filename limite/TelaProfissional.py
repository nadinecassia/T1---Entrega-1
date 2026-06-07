from limite.AbstractTela import AbstractTela


class TelaProfissional(AbstractTela):
    def __init__(self, controlador):
        super().__init__(controlador)

    def mostrar_menu(self) -> int:
        print("\n-------- PROFISSIONAL --------")
        print("1 - Incluir profissional")
        print("2 - Alterar profissional")
        print("3 - Excluir profissional")
        print("4 - Listar profissionais")
        print("0 - Voltar")

        opcao = self.le_num_inteiro("Escolha a opção: ", [1, 2, 3, 4, 0])
        return opcao

    def pegar_dados(self) -> dict:
        print("\n-------- DADOS DO PROFISSIONAL --------")
        nome = self.le_texto_obrigatorio("Nome: ")
        cpf = self.le_texto_obrigatorio("CPF: ")
        celular = self.le_texto_obrigatorio("Celular: ")
        especialidade = self.le_texto_obrigatorio("Especialidade: ")
        registro_profissional = self.le_texto_obrigatorio("Registro profissional: ")

        return {
            "nome": nome,
            "cpf": cpf,
            "celular": celular,
            "especialidade": especialidade,
            "registro_profissional": registro_profissional,
        }

    def mostrar_profissional(self, dados_profissional: dict):
        print("PROFISSIONAL: ", dados_profissional["nome"])
        print("CPF: ", dados_profissional["cpf"])
        print("CELULAR: ", dados_profissional["celular"])
        print("ESPECIALIDADE: ", dados_profissional["especialidade"])
        print("REGISTRO PROFISSIONAL: ", dados_profissional["registro_profissional"])
        print("-" * 30)

    def selecionar(self) -> str:
        print("\n-------- SELECIONAR PROFISSIONAL --------")
        cpf = self.le_texto_obrigatorio("Digite o CPF do profissional: ")
        return cpf
