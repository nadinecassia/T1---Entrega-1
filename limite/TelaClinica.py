from limite.AbstractTela import AbstractTela


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
        nome = input("Nome da clínica: ")
        descricao = input("Descrição: ")
        cidade = input("Cidade (Localização): ")

        return {"nome": nome, "descricao": descricao, "cidade": cidade}

    def mostrar_clinica(self, dados_clinica: dict):
        print("NOME DA CLÍNICA: ", dados_clinica["nome"])
        print("DESCRIÇÃO: ", dados_clinica["descricao"])
        print("CIDADE: ", dados_clinica["cidade"])
        print("-" * 30)

    def selecionar(self) -> str:
        print("\n-------- SELECIONAR CLÍNICA --------")
        nome = input("Digite o nome exato da clínica que deseja selecionar: ")
        return nome

    def mostrar_msg(self, msg: str):
        print(msg)
