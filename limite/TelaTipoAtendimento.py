from limite.AbstractTela import AbstractTela


class TelaTipoAtendimento(AbstractTela):
    def __init__(self, controlador):
        super().__init__(controlador)

    def mostrar_menu(self) -> int:
        print("\n-------- TIPOS DE ATENDIMENTO --------")
        print("1 - Incluir tipo de atendimento")
        print("2 - Alterar tipo de atendimento")
        print("3 - Excluir tipo de atendimento")
        print("4 - Listar tipos de atendimento")
        print("0 - Voltar")

        opcao = self.le_num_inteiro("Escolha a opção: ", [1, 2, 3, 4, 0])
        return opcao

    def pegar_dados(self) -> dict:
        print("\n-------- DADOS DO TIPO DE ATENDIMENTO --------")
        nome = self.le_texto_obrigatorio("Nome: ")
        descricao = self.le_texto_obrigatorio("Descrição: ")

        return {"nome": nome, "descricao": descricao}

    def mostrar_tipo_atendimento(self, dados_tipo: dict):
        print("TIPO DE ATENDIMENTO: ", dados_tipo["nome"])
        print("DESCRIÇÃO: ", dados_tipo["descricao"])
        print("-" * 30)

    def selecionar(self) -> str:
        print("\n-------- SELECIONAR TIPO DE ATENDIMENTO --------")
        nome = self.le_texto_obrigatorio("Digite o nome do tipo de atendimento: ")
        return nome
    
    def mostrar_msg(self, msg: str):
        print(msg)
